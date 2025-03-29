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

" === New Plugins ===
Plug 'mg979/vim-visual-multi', {'branch': 'master'}    " Multiple cursors/selections
Plug 'folke/trouble.nvim'                              " Diagnostics and quickfix UI
Plug 'mfussenegger/nvim-dap'                           " Debugging support (DAP)
Plug 'mfussenegger/nvim-dap-python'                    " Python DAP extension
Plug 'ThePrimeagen/harpoon'                            " Quick file navigation
Plug 'echasnovski/mini.nvim', {'branch': 'stable'}     " Collection of mini enhancements
Plug 'folke/zen-mode.nvim'                             " Distraction-free editing

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
EOF

" === LSP Keybindings ===
nnoremap <silent> gd <cmd>lua vim.lsp.buf.definition()<CR>
nnoremap <silent> K <cmd>lua vim.lsp.buf.hover()<CR>
nnoremap <silent> <leader>rn <cmd>lua vim.lsp.buf.rename()<CR>
nnoremap <silent> <leader>ca <cmd>lua vim.lsp.buf.code_action()<CR>
nnoremap <silent> [d <cmd>lua vim.diagnostic.goto_prev()<CR>
nnoremap <silent> ]d <cmd>lua vim.diagnostic.goto_next()<CR>

" === Diagnostics Display ===
lua vim.diagnostic.config({ virtual_text = true, signs = true })

" === Treesitter Configuration ===
lua << EOF
require('nvim-treesitter.configs').setup {
  ensure_installed = { "c", "cpp", "rust", "python" },
  highlight = { enable = true },
}
EOF

" === Lualine Configuration ===
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
      function() return vim.lsp.get_active_clients()[1] and vim.lsp.get_active_clients()[1].name or '' end
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
  },
  format_on_save = {
    timeout_ms = 500,
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
" No Lua config needed; uses default keybindings (<Ctrl-N>, <Ctrl-Down>)

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
require('dap-python').setup('python')  -- Python debugging with debugpy
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

" === Custom Keybindings ===
nnoremap <C-a> ggVG
nnoremap <leader>ff <cmd>Telescope find_files<CR>
nnoremap <leader>fg <cmd>Telescope live_grep<CR>
nnoremap <leader>n <cmd>NERDTreeToggle<CR>
nnoremap <leader>gs <cmd>Git<CR>
nnoremap <leader>t <cmd>Trouble diagnostics<CR>
nnoremap <leader>db <cmd>lua require('dap').toggle_breakpoint()<CR>
nnoremap <leader>dc <cmd>lua require('dap').continue()<CR>
nnoremap <leader>ha <cmd>lua require('harpoon.mark').add_file()<CR>
nnoremap <leader>hm <cmd>lua require('harpoon.ui').toggle_quick_menu()<CR>
nnoremap <leader>1 <cmd>lua require('harpoon.ui').nav_file(1)<CR>
nnoremap <leader>2 <cmd>lua require('harpoon.ui').nav_file(2)<CR>
nnoremap <leader>z <cmd>ZenMode<CR>             " Open Fugitive Git status
