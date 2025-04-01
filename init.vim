" === General Settings ===
set nocompatible            " Disable compatibility with old vi (modern features enabled)
set showmatch               " Highlight matching parentheses, brackets, etc.
set ignorecase              " Make searches case-insensitive by default
set mouse=v                 " Enable middle-click paste (limited mouse support)
set hlsearch                " Highlight all search matches
set incsearch               " Show search matches as you type
set tabstop=4               " Set tab width to 4 columns
set softtabstop=4           " Treat 4 spaces as a tab for backspace behavior
set expandtab               " Convert tabs to spaces
set shiftwidth=4            " Set indentation width to 4 spaces
set autoindent              " Copy indentation from previous line
set number                  " Show line numbers
syntax on                   " Enable syntax highlighting
set mouse=a                 " Enable full mouse support (click, scroll, etc.)
set clipboard=unnamedplus   " Use system clipboard for yank/delete/paste
filetype plugin on          " Enable filetype-specific plugins
set linebreak               " Break lines at word boundaries (not mid-word)
set ttyfast                 " Optimize for faster terminal redraws
set spell                   " Enable spell checking (language pack may be needed)
set so=5                    " Scroll offset: keep 5 lines visible above/below cursor
set splitright              " Open vertical splits to the right
set splitbelow              " Open horizontal splits below
set encoding=utf-8          " Use UTF-8 encoding for files
set nobackup                " Disable backup files
set nowritebackup           " Disable backup before overwriting files
set signcolumn=yes          " Always show the sign column (for diagnostics, git signs, etc.)
set updatetime=2000         " Set update time to 2 seconds for autosave
set statusline+=%m          " Show modified flag in status line
set confirm                 " Prevent accidental quits with unsaved changes

" === Leader Key ===
let mapleader = " "          " Set leader key to Space (improves ergonomics for keybindings)

" === Plugin Management with vim-plug ===
call plug#begin()

" === Utility Plugins ===
Plug 'junegunn/vim-easy-align', { 'on': 'EasyAlign' }
Plug 'fatih/vim-go', { 'tag': '*', 'for': 'go' }
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'preservim/nerdtree', { 'on': 'NERDTreeToggle' }
Plug 'tpope/vim-fireplace', { 'for': 'clojure' }
Plug 'm4xshen/autoclose.nvim'
Plug 'nsf/gocode', { 'rtp': 'vim', 'for': 'go' }

" === Modern Neovim Plugins ===
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
Plug 'nvim-lua/plenary.nvim'
Plug 'nvim-telescope/telescope.nvim', { 'tag': '0.1.8' }
Plug 'neovim/nvim-lspconfig'
Plug 'hrsh7th/nvim-cmp'
Plug 'hrsh7th/cmp-nvim-lsp'
Plug 'nvim-lualine/lualine.nvim'
Plug 'stevearc/conform.nvim'

" === Colorscheme ===
Plug 'morhetz/gruvbox'

" === Additional Plugins ===
Plug 'numToStr/Comment.nvim'
Plug 'lewis6991/gitsigns.nvim'
Plug 'folke/which-key.nvim'
Plug 'williamboman/mason.nvim'
Plug 'williamboman/mason-lspconfig.nvim'
Plug 'tpope/vim-fugitive'
Plug 'kylechui/nvim-surround'
Plug 'mg979/vim-visual-multi', {'branch': 'master'}
Plug 'folke/trouble.nvim'
Plug 'mfussenegger/nvim-dap'
Plug 'mfussenegger/nvim-dap-python'
Plug 'ThePrimeagen/harpoon'
Plug 'echasnovski/mini.nvim', {'branch': 'stable'}
Plug 'folke/zen-mode.nvim'

" === New Plugins ===
Plug 'vim-test/vim-test'
Plug 'ahmedkhalf/project.nvim'
Plug 'ggandor/leap.nvim'
Plug 'nvim-tree/nvim-tree.lua'
Plug 'arkav/lualine-lsp-progress'

" === Added Plugins ===
Plug 'Pocco81/auto-save.nvim'           " Autosave functionality
Plug 'akinsho/bufferline.nvim'          " Buffer tabs integration
Plug 'folke/persistence.nvim'           " Session management
Plug 'simrat39/rust-tools.nvim'         " Enhanced Rust support

call plug#end()

" === Colorscheme ===
colorscheme gruvbox

" === LSP Configuration ===
lua << EOF
require('lspconfig').clangd.setup {
  cmd = { "clangd", "--background-index" },
  filetypes = { "c", "cpp", "objc", "objcpp" },
}
require('lspconfig').rust_analyzer.setup {
  settings = {
    ["rust-analyzer"] = {
      checkOnSave = { command = "clippy" },
    },
  },
}
require('lspconfig').pyright.setup {
  settings = {
    python = {
      analysis = {
        autoSearchPaths = true,
        useLibraryCodeForTypes = true,
        diagnosticMode = "workspace",
      },
    },
  },
}
require('rust-tools').setup({
  server = {
    settings = {
      ["rust-analyzer"] = {
        checkOnSave = { command = "clippy" },
      },
    },
  },
})
EOF

" === Diagnostics Display ===
lua vim.diagnostic.config({ virtual_text = true, signs = true })

" === Treesitter Configuration ===
lua << EOF
require('nvim-treesitter.configs').setup {
  ensure_installed = { "c", "cpp", "rust", "python", "toml" },
  highlight = { enable = true },
}
EOF

" === Autoclose Configuration ===
lua << EOF
require('autoclose').setup {
  keys = {
    ["("] = { escape = false, close = true, pair = "()" },
    ["["] = { escape = false, close = true, pair = "[]" },
    ["{"] = { escape = false, close = true, pair = "{}" },
    ["<"] = { escape = false, close = true, pair = "<>" },
    ['"'] = { escape = true, close = true, pair = '""' },
    ["'"] = { escape = true, close = true, pair = "''" },
    ["`"] = { escape = true, close = true, pair = "``" },
  },
  options = {
    disable_when_touch = false,
    pair_spaces = true,
  },
}
EOF

" === Custom Highlighting for Braces ===
highlight MatchParen guifg=#fabd2f guibg=NONE gui=bold  " Matching braces (yellow, bold)
highlight TSOperator guifg=#d3869b                    " Curly braces in Rust (pinkish)
autocmd FileType rust highlight TSOperator guifg=#d3869b  " Ensure Rust-specific override

" === Lualine Configuration with LSP Progress ===
lua << EOF
require('lualine').setup {
  options = {
    theme = 'auto',
    section_separators = { left = '', right = '' },
    component_separators = { left = '', right = '' },
  },
  sections = {
    lualine_a = {'mode'},
    lualine_b = {'branch', 'diff', {'diagnostics', sources = {'nvim_lsp'}}},
    lualine_c = {
      'filename',
      function() return vim.lsp.get_active_clients()[1] and vim.lsp.get_active_clients()[1].name or '' end,
      'lsp_progress',
    },
    lualine_x = {'encoding', 'fileformat', 'filetype'},
    lualine_y = {'progress'},
    lualine_z = {'location'}
  },
}
EOF

" === nvim-cmp Configuration ===
lua << EOF
local cmp = require('cmp')
cmp.setup {
  sources = {
    { name = 'nvim_lsp' },
  },
  mapping = {
    ['<CR>'] = cmp.mapping.confirm({ select = true }),
    ['<C-n>'] = cmp.mapping.select_next_item(),
    ['<C-p>'] = cmp.mapping.select_prev_item(),
  },
}
EOF

" === conform.nvim Configuration ===
lua << EOF
require("conform").setup {
  formatters_by_ft = {
    c = { "clang-format" },
    cpp = { "clang-format" },
    rust = { "rustfmt" },
    python = { "black" },
    toml = { "taplo" },
  },
  format_on_save = {
    timeout_ms = 500,
    lsp_fallback = true,
  },
  notify_on_error = true,
  format_after_save = {
    lsp_fallback = true,
  },
}
EOF

" === Comment.nvim Configuration ===
lua << EOF
require('Comment').setup()
EOF

" === gitsigns.nvim Configuration ===
lua << EOF
require('gitsigns').setup {
  signs = {
    add = { text = '+' },
    change = { text = '~' },
    delete = { text = '_' },
  },
}
EOF

" === which-key.nvim Configuration ===
lua << EOF
require('which-key').setup()
EOF

" === mason.nvim Configuration ===
lua << EOF
require('mason').setup()
require('mason-lspconfig').setup {
  ensure_installed = { "clangd", "rust_analyzer", "pyright" },
  automatic_installation = true,
}
EOF

" === nvim-surround Configuration ===
lua << EOF
require('nvim-surround').setup()
EOF

" === vim-visual-multi Configuration ===
" No Lua config needed; uses default bindings

" === trouble.nvim Configuration ===
lua << EOF
require("trouble").setup {
  position = "bottom",
  auto_open = false,
}
EOF

" === nvim-dap Configuration ===
lua << EOF
local dap = require('dap')
dap.adapters.cppdbg = {
  id = 'cppdbg',
  type = 'executable',
  command = '/path/to/cpptools/extension/debugAdapters/bin/OpenDebugAD7',  -- Adjust path
}
dap.configurations.cpp = {
  {
    name = "Launch file",
    type = "cppdbg",
    request = "launch",
    program = function()
      return vim.fn.input('Path to executable: ', vim.fn.getcwd() .. '/', 'file')
    end,
    cwd = '${workspaceFolder}',
    stopAtEntry = true,
  },
}
dap.configurations.c = dap.configurations.cpp
require('dap-python').setup('python')
dap.adapters.lldb = {
  type = 'executable',
  command = '/usr/bin/lldb-vscode', -- Adjust path if needed (install lldb)
  name = 'lldb'
}
dap.configurations.rust = {
  {
    name = 'Launch',
    type = 'lldb',
    request = 'launch',
    program = function()
      return vim.fn.input('Path to executable: ', vim.fn.getcwd() .. '/', 'file')
    end,
    cwd = '${workspaceFolder}',
    stopOnEntry = false,
  },
}
EOF

" === harpoon Configuration ===
lua << EOF
require("harpoon").setup()
EOF

" === mini.nvim Configuration ===
lua << EOF
require('mini.ai').setup()
require('mini.animate').setup()
EOF

" === zen-mode.nvim Configuration ===
lua << EOF
require("zen-mode").setup {
  window = {
    width = 120,
  },
}
EOF

" === vim-test Configuration ===
let test#strategy = "neovim"

" === project.nvim Configuration ===
lua << EOF
require("project_nvim").setup {
  detection_methods = { "lsp", "pattern" },
  patterns = { ".git", "Makefile", "Cargo.toml" },
}
require('telescope').load_extension('projects')
EOF

" === leap.nvim Configuration ===
lua << EOF
require('leap').add_default_mappings(false)  -- Disable default mappings to avoid conflicts
vim.keymap.set({'n', 'x', 'o'}, 'z',  '<Plug>(leap-forward)')  -- Use z for forward jump
vim.keymap.set({'n', 'x', 'o'}, 'Z',  '<Plug>(leap-backward)')  -- Use Z for backward jump
EOF

" === nvim-tree.lua Configuration ===
lua << EOF
require("nvim-tree").setup {
  view = {
    width = 30,
  },
  git = {
    enable = true,
  },
}
EOF

" === auto-save.nvim Configuration ===
lua << EOF
require("auto-save").setup {
  enabled = true,
  execution_message = {
    message = function() return "AutoSave: saved at " .. vim.fn.strftime("%H:%M:%S") end,
    dim = 0.18,
    cleaning_interval = 1250,
  },
  trigger_events = {"InsertLeave", "TextChanged"},
  write_all_buffers = false,
  debounce_delay = 135,
}
EOF

" === bufferline.nvim Configuration ===
lua << EOF
require("bufferline").setup {
  options = {
    diagnostics = "nvim_lsp",
    offsets = {{filetype = "NvimTree", text = "File Explorer"}},
  },
}
EOF

" === persistence.nvim Configuration ===
lua << EOF
require("persistence").setup {
  dir = vim.fn.expand(vim.fn.stdpath("state") .. "/sessions/"),
  options = {"buffers", "curdir", "tabpages", "winsize"}
}
EOF

" === Keybindings ===
" All keybindings are organized alphabetically by prefix within functional groups.

" --- Buffer Management ---
nnoremap <C-a> ggVG                         " Select all text in buffer
nnoremap <leader>b <cmd>BufferLinePick<CR>  " Pick buffer from tabline

" --- Commenting ---
" gcc: Toggle line comment (Comment.nvim)
" gc<motion>: Comment block (e.g., gcip for paragraph)
" gc (Visual mode): Comment selected lines

" --- Debugging ---
nnoremap <leader>db <cmd>lua require('dap').toggle_breakpoint()<CR>  " Toggle breakpoint
nnoremap <leader>dc <cmd>lua require('dap').continue()<CR>           " Start/continue debugging

" --- File Explorer ---
nnoremap <leader>n <cmd>NvimTreeToggle<CR>  " Toggle NvimTree

" --- File Marking (Harpoon) ---
nnoremap <leader>ha <cmd>lua require('harpoon.mark').add_file()<CR>      " Add file to Harpoon
nnoremap <leader>hm <cmd>lua require('harpoon.ui').toggle_quick_menu()<CR>  " Toggle Harpoon menu
nnoremap <leader>1 <cmd>lua require('harpoon.ui').nav_file(1)<CR>        " Jump to first marked file
nnoremap <leader>2 <cmd>lua require('harpoon.ui').nav_file(2)<CR>        " Jump to second marked file

" --- File Navigation (Telescope) ---
nnoremap <leader>ff <cmd>Telescope find_files<CR>  " Find files
nnoremap <leader>fg <cmd>Telescope live_grep<CR>   " Live grep across files
nnoremap <leader>fp <cmd>Telescope projects<CR>    " Find projects

" --- Git Integration ---
nnoremap <leader>gs <cmd>Git<CR>  " Open Git status (vim-fugitive)
" [c: Previous hunk (gitsigns.nvim)
" ]c: Next hunk (gitsigns.nvim)
nnoremap <leader>hb :Gitsigns toggle_current_line_blame<CR>  " Toggle line blame

" --- LSP ---
nnoremap <leader>ca <cmd>lua vim.lsp.buf.code_action()<CR>  " Code action
nnoremap <leader>rn <cmd>lua vim.lsp.buf.rename()<CR>      " Rename symbol
nnoremap [d <cmd>lua vim.diagnostic.goto_prev()<CR>        " Previous diagnostic
nnoremap ]d <cmd>lua vim.diagnostic.goto_next()<CR>        " Next diagnostic
nnoremap gd <cmd>lua vim.lsp.buf.definition()<CR>          " Go to definition
nnoremap K <cmd>lua vim.lsp.buf.hover()<CR>                " Hover info

" --- Multiple Cursors (vim-visual-multi) ---
" <Ctrl-N>: Start multi-cursor on word, repeat for more
" <Ctrl-Down>: Add cursor below
" <Ctrl-Up>: Add cursor above
" <Tab>: Switch between cursor and selection modes

" --- Session Management ---
nnoremap <leader>sl <cmd>lua require('persistence').load({last=true})<CR>  " Restore last session
nnoremap <leader>ss <cmd>lua require('persistence').load()<CR>            " Restore session

" --- Testing (vim-test) ---
nnoremap <leader>tf <cmd>TestFile<CR>     " Run all tests in file
nnoremap <leader>tn <cmd>TestNearest<CR>  " Run nearest test
nnoremap <leader>ts <cmd>TestSuite<CR>    " Run entire test suite

" --- Diagnostics UI ---
nnoremap <leader>t <cmd>Trouble diagnostics<CR>  " Open diagnostics list

" --- Zen Mode ---
nnoremap <leader>z <cmd>ZenMode<CR>  " Toggle Zen Mode
