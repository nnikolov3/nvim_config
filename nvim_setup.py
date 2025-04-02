#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
from textwrap import dedent
import time

# --- Configuration ---
NVIM_CONFIG_DIR = Path.home() / ".config" / "nvim"
NVIM_SHARE_DIR = Path.home() / ".local" / "share" / "nvim"
NVIM_STATE_DIR = Path.home() / ".local" / "state" / "nvim"
BACKUP_BASE_DIR = Path.home() / "nvim_backups"

# --- Minimal Configuration Content ---
config_files_content = {
    Path("init.lua"): """
        -- ~/.config/nvim/init.lua
        vim.g.mapleader = ' '
        vim.g.maplocalleader = ' '

        -- Load core configurations
        require('config.options')
        require('config.keymaps')
        require('config.autocmds')

        -- Bootstrap lazy.nvim
        require('config.lazy')
    """,
    Path("lua/config/options.lua"): """
        -- ~/.config/nvim/lua/config/options.lua
        local opt = vim.opt

        -- General
        opt.mouse = 'a'
        opt.clipboard = 'unnamedplus'
        opt.swapfile = false
        opt.backup = false
        opt.undofile = true
        opt.undodir = vim.fn.stdpath('data') .. '/undodir'
        if not vim.loop.fs_stat(vim.fn.stdpath('data') .. '/undodir') then
          vim.fn.mkdir(vim.fn.stdpath('data') .. '/undodir', 'p')
        end

        -- UI
        opt.number = true
        opt.relativenumber = true
        opt.signcolumn = 'yes'
        opt.showmatch = true
        opt.foldmethod = 'marker'
        opt.colorcolumn = '80'
        opt.termguicolors = true
        opt.cursorline = true
        opt.scrolloff = 5

        -- Tabs & Indentation
        opt.expandtab = true
        opt.shiftwidth = 4
        opt.tabstop = 4
        opt.softtabstop = 4
        opt.autoindent = true
        opt.smartindent = true

        print('Core options loaded')
    """,
    Path("lua/config/keymaps.lua"): """
        -- ~/.config/nvim/lua/config/keymaps.lua
        local map = vim.keymap.set
        local opts = { noremap = true, silent = true }

        print('Loading core keymaps...')

        -- General
        map('n', '<Esc>', '<cmd>noh<CR><Esc>', { desc = 'Clear search highlight' })
        map('n', '<leader>w', '<cmd>w<CR>', { desc = 'Save buffer' })
        map('n', '<leader>q', '<cmd>q<CR>', { desc = 'Quit window' })

        -- Window navigation
        map('n', '<C-h>', '<C-w>h', { desc = 'Navigate Left Pane' })
        map('n', '<C-j>', '<C-w>j', { desc = 'Navigate Down Pane' })
        map('n', '<C-k>', '<C-w>k', { desc = 'Navigate Up Pane' })
        map('n', '<C-l>', '<C-w>l', { desc = 'Navigate Right Pane' })

        print('Core keymaps loaded.')
    """,
    Path("lua/config/autocmds.lua"): """
        -- ~/.config/nvim/lua/config/autocmds.lua
        local api = vim.api

        -- Highlight yanked text
        api.nvim_create_autocmd('TextYankPost', {
          callback = function()
            vim.highlight.on_yank({ higroup = 'IncSearch', timeout = 200 })
          end,
          desc = 'Highlight yanked text',
        })

        print('Autocommands loaded.')
    """,
    Path("lua/config/lazy.lua"): """
        -- ~/.config/nvim/lua/config/lazy.lua
        local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
        if not vim.loop.fs_stat(lazypath) then
          print('Installing lazy.nvim...')
          vim.fn.system({
            'git',
            'clone',
            '--filter=blob:none',
            'https://github.com/folke/lazy.nvim.git',
            '--branch=stable',
            lazypath,
          })
          print('lazy.nvim installed.')
        end
        vim.opt.rtp:prepend(lazypath)

        require('lazy').setup({
          -- Theme
          {
            'morhetz/gruvbox',
            priority = 1000,
            config = function()
              vim.opt.background = 'dark'
              vim.cmd.colorscheme('gruvbox')
              print('Gruvbox theme configured.')
            end,
          },
          -- File Explorer
          {
            'nvim-tree/nvim-tree.lua',
            dependencies = { 'nvim-tree/nvim-web-devicons' },
            keys = {
              { '<leader>e', '<cmd>NvimTreeToggle<cr>', desc = 'Toggle NvimTree Explorer' },
            },
            config = function()
              vim.g.loaded_netrw = 1
              vim.g.loaded_netrwPlugin = 1
              require('nvim-tree').setup({
                view = { width = 30, side = 'left' },
                filters = { dotfiles = false },
              })
              print('NvimTree configured')
            end,
          },
          -- LSP Support
          {
            'neovim/nvim-lspconfig',
            dependencies = {
              { 'williamboman/mason.nvim', config = true },
              { 'williamboman/mason-lspconfig.nvim' },
            },
            config = function()
              local lspconfig = require('lspconfig')
              local mason_lspconfig = require('mason-lspconfig')

              mason_lspconfig.setup({
                ensure_installed = { 'lua_ls', 'pyright' },
                automatic_installation = true,
              })

              local on_attach = function(client, bufnr)
                local map = vim.keymap.set
                local bufopts = { noremap = true, silent = true, buffer = bufnr }
                map('n', 'gd', vim.lsp.buf.definition, vim.tbl_extend('force', bufopts, { desc = 'Go to Definition' }))
                map('n', 'K', vim.lsp.buf.hover, vim.tbl_extend('force', bufopts, { desc = 'Hover Documentation' }))
                print('LSP attached: ' .. client.name)
              end

              mason_lspconfig.setup_handlers({
                function(server_name)
                  lspconfig[server_name].setup({
                    on_attach = on_attach,
                  })
                end,
                ['lua_ls'] = function()
                  lspconfig.lua_ls.setup({
                    on_attach = on_attach,
                    settings = {
                      Lua = {
                        diagnostics = { globals = { 'vim' } },
                        telemetry = { enable = false },
                      },
                    },
                  })
                end,
              })

              print('LSP configured')
            end,
          },
        }, {
          checker = { enabled = true, notify = false },
          change_detection = { enabled = true, notify = true },
        })

        print('lazy.nvim configured.')
    """,
}

# --- Helper Functions ---
def print_error(msg):
    print(f"\033[91mERROR: {msg}\033[0m", file=sys.stderr)

def print_success(msg):
    print(f"\033[92mSUCCESS: {msg}\033[0m")

def print_warning(msg):
    print(f"\033[93mWARNING: {msg}\033[0m")

def print_info(msg):
    print(f"\033[94mINFO: {msg}\033[0m")

def confirm(prompt):
    while True:
        response = input(f"{prompt} [y/N]: ").lower().strip()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no', ''):
            return False
        else:
            print("Please answer 'yes' or 'no'.")

def check_permissions(path):
    """Check if the path is writable."""
    try:
        if path.exists():
            return os.access(path, os.W_OK)
        else:
            parent = path.parent
            parent.mkdir(parents=True, exist_ok=True)
            return os.access(parent, os.W_OK)
    except Exception as e:
        print_error(f"Permission check failed for {path}: {e}")
        return False

def list_directory_contents(path):
    """List the contents of the directory recursively."""
    print_info(f"Listing contents of {path}:")
    try:
        for item in path.rglob("*"):
            if item.is_file():
                print(f"  - File: {item}")
            elif item.is_dir():
                print(f"  - Dir: {item}")
    except Exception as e:
        print_error(f"Failed to list directory contents: {e}")

# --- Core Functions ---
def backup_config(config_dir, share_dir, state_dir, backup_base_dir):
    """Backs up existing Neovim config, share, and state directories."""
    if not check_permissions(backup_base_dir):
        print_error(f"No write permission for backup directory: {backup_base_dir}")
        return False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = backup_base_dir / f"nvim_backup_{timestamp}"

    print_info("Preparing backup...")
    backup_items = []
    for dir_path in (config_dir, share_dir, state_dir):
        if dir_path.exists():
            backup_items.append(dir_path)
            print(f"  - Found: {dir_path}")

    if not backup_items:
        print_warning("No existing Neovim configuration found to back up.")
        return True

    if not confirm(f"Backup existing config to '{backup_dir}'?"):
        print_warning("Backup aborted by user. Proceeding with setup...")
        return True  # Continue even if backup is aborted

    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        for item in backup_items:
            destination = backup_dir / item.name
            print(f"  - Backing up {item.name} to {destination}...")
            if item.is_dir():
                shutil.copytree(item, destination, symlinks=True, dirs_exist_ok=True)
            else:
                shutil.copy2(item, destination)
        print_success(f"Backup completed successfully to {backup_dir}")
        return True
    except Exception as e:
        print_error(f"Backup failed: {e}")
        return False

def cleanup_old_config(config_dir, share_dir, state_dir):
    """Removes existing Neovim configuration files/dirs."""
    if not check_permissions(config_dir):
        print_error(f"No write permission for config directory: {config_dir}")
        return False

    if not confirm("Proceed with removing existing configuration files/dirs?"):
        print_warning("Cleanup aborted by user. Proceeding with setup...")
        return True

    print_info("Cleaning up existing configuration...")
    items_to_remove = [config_dir, share_dir, state_dir]
    removed_count = 0
    for item in items_to_remove:
        try:
            if item.exists():
                if item.is_file() or item.is_symlink():
                    item.unlink()
                    print(f"  - Removed file: {item}")
                    removed_count += 1
                elif item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                    print(f"  - Removed directory: {item}")
                    removed_count += 1
        except Exception as e:
            print_error(f"Failed to remove {item}: {e}")

    if removed_count > 0:
        print_success("Cleanup finished.")
    else:
        print_info("No existing configuration items found to clean up.")
    return True

def setup_new_config(config_dir, files_content):
    """Creates the new directory structure and writes the configuration files."""
    if not check_permissions(config_dir):
        print_error(f"No write permission for config directory: {config_dir}")
        return False

    print_info("Setting up new Neovim configuration...")
    try:
        for relative_path, content in files_content.items():
            full_path = config_dir / relative_path
            print(f"  - Creating {full_path}...")
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(dedent(content).strip(), encoding='utf-8')
            # Verify the file was created
            if full_path.exists():
                print(f"    - Successfully created: {full_path}")
            else:
                print_error(f"    - Failed to create: {full_path}")
                return False
        print_success("New configuration files created.")
        # List directory contents to confirm
        list_directory_contents(config_dir)
        return True
    except Exception as e:
        print_error(f"Failed to set up new configuration: {e}")
        return False

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Neovim Lua Configuration Setup ---")
    print(f"Target Neovim config directory: {NVIM_CONFIG_DIR}")
    print("-" * 38)

    # Check Python version
    if sys.version_info < (3, 8):
        print_error("Python 3.8 or higher is required.")
        sys.exit(1)

    # 1. Backup
    if not backup_config(NVIM_CONFIG_DIR, NVIM_SHARE_DIR, NVIM_STATE_DIR, BACKUP_BASE_DIR):
        print_warning("Backup failed. Proceeding with setup...")
        # Continue even if backup fails

    print("-" * 38)
    time.sleep(0.5)

    # 2. Cleanup
    if not cleanup_old_config(NVIM_CONFIG_DIR, NVIM_SHARE_DIR, NVIM_STATE_DIR):
        print_warning("Cleanup skipped or failed. Proceeding with setup...")

    print("-" * 38)
    time.sleep(0.5)

    # 3. Setup New Configuration
    if not setup_new_config(NVIM_CONFIG_DIR, config_files_content):
        sys.exit(1)

    print("-" * 38)
    print_success("Neovim configuration setup complete!")
    print("\nNext Steps:")
    print("1. Launch Neovim (`nvim`).")
    print("2. Wait for lazy.nvim to install plugins (this happens automatically).")
    print("   - If plugins don’t install, run `:Lazy sync`.")
    print("3. Restart Neovim after plugin installation.")
    print("4. Run `:checkhealth` to diagnose any issues.")
    print("5. Run `:Mason` to verify LSP installations (e.g., lua_ls, pyright).")
    print("6. Test the setup:")
    print("   - Open a Lua file to check if LSP (lua_ls) works.")
    print("   - Press `<leader>e` (space + e) to toggle the file explorer.")
    print("   - The Gruvbox theme should be applied automatically.")
    print("--- Enjoy your new Neovim setup! ---")
