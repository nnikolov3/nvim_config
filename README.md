# Neovim Hotkeys and Functionality Guide

This guide covers the keybindings and features of your Neovim setup, which is configured using two Python scripts: `setup_nvim.py` and `tool_setup.py`. The setup includes plugins for LSP, formatting, debugging, navigation, Git integration, testing, autosave, buffer management, session persistence, and Linux kernel development. Your leader key is `<Space>` (set with `vim.g.mapleader = ' '` in `init.lua`).

---

## Setup Scripts Overview

### `setup_nvim.py`
- **Purpose**: Configures Neovim with a modern Lua-based setup.
- **Functionality**:
  - Backs up existing Neovim configuration directories (`~/.config/nvim`, `~/.local/share/nvim`, `~/.local/state/nvim`) to `~/nvim_backups`.
  - Cleans up old configuration files (e.g., `init.vim`, `lua/`, `plugged/`).
  - Sets up a new configuration with `lazy.nvim` as the plugin manager.
  - Installs essential plugins: `nvim-lspconfig`, `nvim-tree`, `telescope`, `nvim-treesitter`, `conform.nvim`, `nvim-dap`, `gitsigns`, `lualine`, `bufferline`, `which-key`, `trouble`, `harpoon`, `zen-mode`, `vim-test`, `persistence`, `leap`, `mini`, `comment`, `surround`, `vim-visual-multi`, `vim-easy-align`, `autoclose`, and more.
  - Configures plugins for Linux kernel development: `vim-linux-coding-style` and `cscope.nvim`.
- **Usage**:
  - Run `chmod +x setup_nvim.py` to make the script executable.
  - Execute `./setup_nvim.py` to set up your Neovim configuration.
  - Follow the prompts to back up and clean up existing configurations.

### `tool_setup.py`
- **Purpose**: Installs all necessary tools and dependencies for the Neovim setup on Linux.
- **Functionality**:
  - Detects the Linux distribution (Red Hat-based like Fedora, or Debian-based like Ubuntu).
  - Installs system packages using `dnf` (Red Hat) or `apt` (Debian):
    - General tools: `neovim`, `git`, `curl`, `unzip`, `nodejs`, `npm`, `python3`, `pip`, `gcc`, `make`, `ripgrep`, `fd-find`, `clang`, `bash`, `shfmt`.
    - Linux kernel development tools: `sparse`, `cscope`, `ctags`, `gdb`, `crash`, `qemu-system-x86`, `strace`, `ltrace`, `kernel-devel` (or `linux-headers`), `ncurses-devel`.
  - Installs additional tools:
    - `rustup` (for `rust_analyzer`, `rustfmt`, `stylua`).
    - `go` (for `gopls`, `gofmt`, `goimports`, `delve`).
    - `lazygit` (for Git integration).
    - `golangci-lint` (for Go linting).
    - Python packages via `pip`: `black`, `isort`.
    - Node.js packages via `npm`: `prettier`.
    - `stylua` via `cargo` (for Lua formatting).
  - Verifies all tools are installed and reports any missing ones.
- **Usage**:
  - Run `chmod +x tool_setup.py` to make the script executable.
  - Execute `./tool_setup.py` to install the tools.
  - Follow the prompts to confirm the installation of packages (requires `sudo`).

---

## General Neovim Hotkeys
- `<Esc>`: **Clear Search Highlight** - Clears search highlights (`:noh`).
- `<C-a>`: **Select All** - Visually select entire buffer (`ggVG`).
- `<Space>w`: **Save Buffer** - Save the current buffer (`:w`).
- `<Space>q`: **Quit Window** - Quit the current window (`:q`).
- `/<pattern>`: Search (with `hlsearch` and `incsearch` enabled).
- `n`/`N`: Next/previous search match (centers screen with `zz`).

---

## LSP (nvim-lspconfig + rust-tools.nvim)
- **Purpose**: Language server support for code navigation, diagnostics, completion, and Rust-specific enhancements.
- **Languages**: C/C++ (`clangd`), Rust (`rust_analyzer` via `rust-tools`), Python (`pyright`), Go (`gopls`), JavaScript/TypeScript (`tsserver`), and more.

### Hotkeys
- `gd`: **Go to Definition** - Jump to symbol definition.
- `K`: **Hover** - Show documentation or type info under cursor.
- `<C-k>`: **Signature Help** - Show function signature help.
- `<Space>rn`: **Rename** - Rename symbol across project.
- `<Space>ca`: **Code Action** - Trigger fixes or refactorings (e.g., Rust imports).
- `gr`: **Go to References** - Show all references to the symbol.
- `[d`: **Previous Diagnostic** - Jump to previous error/warning.
- `]d`: **Next Diagnostic** - Jump to next error/warning.
- `<Space>do`: **Show Line Diagnostics** - Display diagnostics for the current line in a floating window.

### Features
- Inline diagnostics shown via `virtual_text` and `signcolumn`.
- Rust-specific features from `rust-tools.nvim`: inlay hints, advanced code actions, and tighter `rust_analyzer` integration.
- LSP servers installed via `mason.nvim`: `lua_ls`, `pyright`, `rust_analyzer`, `gopls`, `tsserver`, etc.

---

## Autocompletion (nvim-cmp)
- **Purpose**: LSP-driven autocompletion with snippet support.

### Hotkeys
- `<CR>` (Enter): Confirm selected completion.
- `<C-j>`: Next completion item.
- `<C-k>`: Previous completion item.
- `<C-Space>`: Trigger completion manually.
- `<Tab>`: Select next item or expand snippet.
- `<S-Tab>`: Select previous item or jump back in snippet.

### Features
- Autocompletion triggered as you type, powered by LSP, buffer, path, and snippet sources.
- Snippet support via `luasnip` (includes VSCode-style snippets from `friendly-snippets`).

---

## Autosave (auto-save.nvim)
- **Purpose**: Automatically save changes to avoid data loss.

### Features
- Saves on `InsertLeave` and `TextChanged` events.
- 200ms debounce delay to prevent excessive writes.
- Displays "AutoSave: HH:MM:SS" in the statusline.

---

## Formatting (conform.nvim)
- **Purpose**: Auto-format code on save using external tools.
- **Tools**: `clang-format` (C/C++), `rustfmt` (Rust), `black` (Python), `gofmt` (Go), `prettier` (JavaScript/TypeScript), `stylua` (Lua), `shfmt` (shell), `nasmfmt` (assembly).

### Hotkeys
- `<Space>f`: **Format Code** - Manually trigger formatting.

### Features
- Formats on save with 750ms timeout.
- Falls back to LSP formatting if the tool fails.
- Error notifications enabled.

---

## File Navigation (telescope.nvim)
- **Purpose**: Fuzzy finding for files, text, projects, and more.

### Hotkeys
- `<Space>ff`: **Find Files** - Search and open files in current directory.
- `<Space>fg`: **Live Grep** - Search text across all files.
- `<Space>fb`: **Find Buffers** - List open buffers.
- `<Space>fh`: **Find Help Tags** - Search Neovim help.
- `<Space>fo`: **Find Recent Files** - List recently opened files.
- `<Space>fp`: **Find Projects** - List and switch between projects (via `project.nvim`).
- `<Space>f/`: **Fuzzy Find in Buffer** - Search within the current buffer.
- `<Space>fr`: **Resume Last Telescope** - Reopen the last Telescope picker.
- `<Space>fk`: **Show Keymaps** - List all keymaps.
- `<Space>fc`: **Show Commands** - List available commands.
- `<Space>f:`: **Command History** - Show command history.
- `<Space>fd`: **Show Diagnostics** - List diagnostics.

### Features
- Fast, interactive UI with Telescope integration.
- Enhanced with `ripgrep` (`rg`) for fast searching and `fd` for file finding.
- Project-aware navigation (via `project.nvim`).

---

## File Explorer (nvim-tree.lua)
- **Purpose**: Modern tree-style file explorer.

### Hotkeys
- `<Space>e`: **Toggle NvimTree** - Show/hide file explorer.
- `<Space>E`: **Toggle NvimTree Find File** - Open explorer and focus on current file.

### Features
- Navigate with arrow keys or mouse.
- Git status integration for files.
- Auto-closes when opening a file.

---

## Buffer Management (bufferline.nvim)
- **Purpose**: Visual buffer tabs with diagnostics.

### Hotkeys
- `<Space>bp`: **Pick Buffer** - Select a buffer from the tabline.
- `<Space>bc`: **Close Current Buffer** - Close the current buffer.
- `<Space>bC`: **Close Other Buffers** - Close all buffers except the current one.
- `[b`: **Previous Buffer** - Cycle to the previous buffer.
- `]b`: **Next Buffer** - Cycle to the next buffer.
- `<Space>b1` to `<Space>b9`: **Go to Buffer 1-9** - Jump to a specific buffer.
- `<Space>b$`: **Go to Last Buffer** - Jump to the last buffer.

### Features
- Shows LSP diagnostics in tabs.
- Offsets for NvimTree integration.

---

## Session Management (persistence.nvim)
- **Purpose**: Save and restore editing sessions.

### Hotkeys
- `<Space>qs`: **Restore Session** - Load session for current directory.
- `<Space>ql`: **Restore Last Session** - Load most recent session.
- `<Space>qd`: **Don't Save Session** - Disable session saving on exit.

### Features
- Saves buffers, cursor positions, tabs, and window sizes.
- Stores sessions in `~/.local/state/nvim/sessions/`.

---

## Git Integration
### neogit
- **Purpose**: Full Git workflow inside Neovim.

#### Hotkeys
- `<Space>gg`: **Open Neogit Status** - Open Neogit status window.

#### Features
- Run Git commands (e.g., commit, push) directly.
- Integrates with Telescope for enhanced UI.

### gitsigns.nvim
- **Purpose**: Git signs and hunk navigation.

#### Hotkeys
- `[c`: **Previous Hunk** - Jump to the previous Git hunk.
- `]c`: **Next Hunk** - Jump to the next Git hunk.
- `<Space>hs`: **Stage Hunk** - Stage the current hunk.
- `<Space>hr`: **Reset Hunk** - Reset the current hunk.
- `<Space>hS`: **Stage Buffer** - Stage all changes in the current buffer.
- `<Space>hU`: **Undo Stage Hunk** - Undo staging of the current hunk.
- `<Space>hR`: **Reset Buffer** - Reset all changes in the current buffer.
- `<Space>hp`: **Preview Hunk** - Preview the current hunk.
- `<Space>hb`: **Blame Line** - Show blame for the current line.
- `<Space>hB`: **Toggle Line Blame** - Toggle line blame display.
- `<Space>hd`: **Diff This File** - Show diff for the current file.
- `<Space>hD`: **Diff This ~** - Show diff against the previous commit.
- `<Space>ht`: **Toggle Deleted View** - Toggle display of deleted lines.

#### Features
- Signs in `signcolumn`: `│` (added), `│` (changed), `_` (deleted).
- Inline blame with `gitsigns.nvim`.

---

## Commenting (Comment.nvim)
- **Purpose**: Quick commenting/uncommenting.

### Hotkeys
- `gcc`: **Toggle Line Comment** - Comment/uncomment current line.
- `gc<motion>`: **Comment Block** - Comment a range (e.g., `gcip` for paragraph).
- `gc` (Visual mode): **Comment Selected Lines** - Comment selected lines.
- `gbc`: **Toggle Block Comment** - Comment/uncomment current line as a block.
- `gb<motion>`: **Comment Block (Blockwise)** - Comment a range as a block.

### Features
- Treesitter-aware commenting for accurate syntax (supports C, Rust, etc.).

---

## Surround (nvim-surround)
- **Purpose**: Add, change, or delete surrounding pairs (e.g., quotes, brackets).

### Hotkeys
- `ys<motion><char>`: **Add Surround** - Surround motion with char (e.g., `ysiw"` adds quotes around word).
- `cs<old><new>`: **Change Surround** - Replace old with new (e.g., `cs"'` changes `"` to `'`).
- `ds<char>`: **Delete Surround** - Remove surrounding char (e.g., `ds"` removes quotes).

### Features
- Supports any pair (parentheses, tags, etc.).

---

## Multiple Cursors (vim-visual-multi)
- **Purpose**: Edit multiple locations simultaneously.

### Hotkeys
- `<Ctrl-N>`: **Start Multi-Cursor** - Select word under cursor, press again for more occurrences.
- `<Ctrl-Down>`/`<Ctrl-Up>`: Add cursor below/above.
- `<Tab>`: Switch between cursor and selection modes.

### Features
- Type once, apply to all selected locations.

---

## Diagnostics UI (trouble.nvim)
- **Purpose**: Interactive diagnostics list.

### Hotkeys
- `<Space>xx`: **Toggle Trouble** - Show all diagnostics.
- `<Space>xw`: **Workspace Diagnostics** - Show workspace diagnostics.
- `<Space>xd`: **Document Diagnostics** - Show document diagnostics.
- `<Space>xl`: **Location List** - Show location list.
- `<Space>xq`: **Quickfix List** - Show quickfix list.
- `gR`: **LSP References** - Show LSP references in Trouble.

### Features
- Navigate diagnostics with arrow keys, open files with Enter.

---

## Debugging (nvim-dap)
- **Purpose**: Debug code with breakpoints and stepping.
- **Languages**: C/C++ (`cppdbg`), Python (`debugpy`), Rust (`codelldb`), Go (`delve`).

### Hotkeys
- `<Space>db`: **Toggle Breakpoint** - Add/remove breakpoint at cursor.
- `<Space>dB`: **Conditional Breakpoint** - Set a breakpoint with a condition.
- `<Space>dl`: **Run Last** - Rerun the last debug session.
- `<Space>dc`: **Continue** - Start or resume debugging.
- `<Space>do`: **Step Over** - Step over the current line.
- `<Space>di`: **Step Into** - Step into a function call.
- `<Space>du`: **Step Out** - Step out of the current function.
- `<Space>dr`: **Open REPL** - Open the DAP REPL.
- `<Space>dt`: **Terminate** - Terminate the debug session.
- `<Space>ds`: **Session Info** - Print session information.
- `<Space>dui`: **Toggle DAP UI** - Show/hide the DAP UI.
- `<Space>due`: **Eval Float** - Show a floating window with variable scopes.

### Features
- Step through code, inspect variables.
- Rust debugging via `codelldb` (installed via `mason-nvim-dap`).
- Python debugging via `debugpy`.
- Go debugging via `delve`.

---

## File Marking (harpoon)
- **Purpose**: Quick navigation between marked files.

### Hotkeys
- `<Space>ha`: **Add File** - Mark current file.
- `<Space>hm`: **Toggle Menu** - Show marked files list.
- `<Space>h1` to `<Space>h4`: **Jump to File 1-4** - Jump to a specific marked file.
- `<Space>hn`: **Next File** - Cycle to the next marked file.
- `<Space>hp`: **Previous File** - Cycle to the previous marked file.

### Features
- Persistent file bookmarks for fast switching.

---

## Mini Enhancements (mini.nvim)
- **Purpose**: Small, modular improvements.

### Features
- `mini.ai`: Enhanced text objects (e.g., `va,` for arguments).
- `mini.animate`: Smooth scrolling and cursor animations.

### Hotkeys
- No new bindings; enhances existing motions (e.g., `viw`, `va(`).

---

## Zen Mode (zen-mode.nvim)
- **Purpose**: Distraction-free editing.

### Hotkeys
- `<Space>z`: **Toggle Zen Mode** - Center buffer, hide UI elements.

### Features
- Fixed 100-column width for focused coding.
- Disables UI elements like `lualine` and `bufferline`.

---

## Testing (vim-test)
- **Purpose**: Run tests directly from Neovim.
- **Frameworks**: pytest (Python), Cargo (Rust), Go tests.

### Hotkeys
- `<Space>tn`: **Test Nearest** - Run test under cursor.
- `<Space>tf`: **Test File** - Run all tests in current file.
- `<Space>ts`: **Test Suite** - Run entire test suite.
- `<Space>tl`: **Run Last Test** - Rerun the last test.
- `<Space>tv`: **Visit Test File** - Jump to the test file.

### Features
- Runs in Neovim terminal (via `test#strategy = "neovim"`).

---

## Project Management (project.nvim)
- **Purpose**: Detect and manage projects, integrate with Telescope.

### Hotkeys
- `<Space>fp`: **Find Projects** - List and switch between projects.

### Features
- Auto-detects projects via LSP or patterns (e.g., `.git`, `Cargo.toml`).
- Syncs with `nvim-tree` for project-aware navigation.

---

## Fast Navigation (leap.nvim)
- **Purpose**: Jump to any visible location with minimal keystrokes.

### Hotkeys
- `s<char><char>`: **Jump Forward** - Jump to first occurrence of two characters (e.g., `sab` jumps to "ab").
- `S<char><char>`: **Jump Backward** - Jump to previous occurrence.
- `gs<char><char>`: **Jump Cross Window** - Jump to a location in another window.

### Features
- Works in normal, visual, and operator-pending modes.
- Highlights jump targets for selection.

---

## Syntax Highlighting (nvim-treesitter)
- **Purpose**: Advanced syntax highlighting and parsing.
- **Languages**: C, C++, Rust, Python, Go, JavaScript, TypeScript, Lua, TOML, and more.

### Hotkeys
- `<C-space>`: **Start Incremental Selection** - Start selecting a syntax node.
- `<C-space>`: **Expand Selection** - Expand the selection to a larger node.
- `<BS>`: **Shrink Selection** - Shrink the selection to a smaller node.
- `]f`/`[f`: **Next/Previous Function** - Jump to the next/previous function.
- `]c`/`[c`: **Next/Previous Class** - Jump to the next/previous class.

### Features
- Precise highlighting for code and config files (e.g., `Cargo.toml`).
- Powers plugins like `Comment.nvim` for context-aware commenting.
- Incremental selection for precise code manipulation.

---

## Linux Kernel Development
- **Purpose**: Enhance Neovim for Linux kernel coding and debugging.

### Plugins
- `vim-linux-coding-style`: Enforces Linux kernel coding style for C files.
- `cscope.nvim`: Integrates `cscope` for code navigation, with Telescope as the picker.

### Hotkeys
- `<Space>cs`: **Cscope Find Symbol** - Find all occurrences of the symbol under cursor.
- `<Space>cg`: **Cscope Find Definition** - Jump to the definition of the symbol under cursor.
- `<Space>cc`: **Cscope Find Callers** - Find all callers of the function under cursor.

### Features
- Coding style enforcement for Linux kernel C files (via `vim-linux-coding-style`).
- Fast code navigation with `cscope` and Telescope integration.
- Tools installed: `sparse` (static analysis), `cscope`, `ctags`, `gdb` (debugging), `crash` (crash dump analysis), `qemu-system-x86` (testing), `strace`, `ltrace` (tracing).

---

## Learning Tips
1. **Explore with Which-Key**: Press `<Space>` and wait to see available bindings (via `which-key.nvim`).
2. **Leverage Autosave**: Edit freely; `auto-save.nvim` handles saving (check statusline for confirmation).
3. **Manage Buffers**: Use `<Space>bp` to switch buffers visually with `bufferline.nvim`.
4. **Restore Sessions**: Use `<Space>qs` or `<Space>ql` to pick up where you left off.
5. **Practice Debugging**: Set a breakpoint (`<Space>db`), start with `<Space>dc`, explore DAP UI with `<Space>dui`.
6. **Format on Save**: Test `conform.nvim` by editing and saving files (e.g., Rust with `rustfmt`).
7. **Multi-Cursor**: Try `<Ctrl-N>` on a repeated word, then edit all instances.
8. **Git Workflow**: Use `<Space>gg` for Neogit status, then commit or push.
9. **Rust Tools**: Hover (`K`) over Rust code to see inlay hints or type info (via `rust-tools`).
10. **Linux Kernel Development**:
    - Navigate to your kernel source (e.g., `/usr/src/linux`).
    - Generate a `cscope` database: `cscope -R -b -q`.
    - Use `<Space>cs` to find symbols, `<Space>cg` to find definitions.
    - Use `sparse` for static analysis: `make C=1 CHECK=sparse`.

---

## Customization
- Adjust keybindings in `lua/config/keymaps.lua` if conflicts arise (e.g., change `<Space>xx` to `<Space>td`).
- Update DAP configurations in `lua/plugins/dap.lua` (e.g., paths for `codelldb` or `debugpy`).
- Experiment with `mini.nvim` modules (e.g., `mini.statusline`).
- Configure `qemu` for kernel testing or `kdump` for crash dump analysis (requires additional setup).
