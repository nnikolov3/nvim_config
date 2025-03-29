# Neovim Hotkeys and Functionality Guide

This guide covers the keybindings and features of your Neovim setup as of your latest `init.vim`. It includes plugins for LSP, formatting, debugging, navigation, and more. Your leader key is `<Space>` (set with `let mapleader = " "`).

---

## General Neovim Hotkeys
- `<C-a>`: **Select All** - Visually select entire buffer (`ggVG`).
- `:w`: Save file.
- `:q`: Quit.
- `/<pattern>`: Search (with `hlsearch` and `incsearch` enabled).
- `n`/`N`: Next/previous search match.

---

## LSP (nvim-lspconfig)
- **Purpose**: Language server support for code navigation, diagnostics, and completion.
- **Languages**: C/C++ (`clangd`), Rust (`rust-analyzer`), Python (`pyright`).

### Hotkeys
- `gd`: **Go to Definition** - Jump to symbol definition.
- `K`: **Hover** - Show documentation or type info under cursor.
- `<Space>rn`: **Rename** - Rename symbol across project.
- `<Space>ca`: **Code Action** - Trigger fixes or refactorings (e.g., Rust imports).
- `[d`: **Previous Diagnostic** - Jump to previous error/warning.
- `]d`: **Next Diagnostic** - Jump to next error/warning.

### Features
- Inline diagnostics (errors/warnings) shown via `virtual_text` and `signcolumn`.

---

## Autocompletion (nvim-cmp)
- **Purpose**: LSP-driven autocompletion.

### Hotkeys
- `<CR>` (Enter): Confirm selected completion.
- `<C-n>`: Next completion item.
- `<C-p>`: Previous completion item.

### Features
- Autocompletion triggered as you type (powered by LSP).

---

## Formatting (conform.nvim)
- **Purpose**: Auto-format code on save using external tools.
- **Tools**: `clang-format` (C/C++), `rustfmt` (Rust), `black` (Python).

### Features
- Formats on save with 500ms timeout.
- Falls back to LSP formatting if the tool fails.

---

## File Navigation (telescope.nvim)
- **Purpose**: Fuzzy finding for files, text, and more.

### Hotkeys
- `<Space>ff`: **Find Files** - Search and open files in current directory.
- `<Space>fg`: **Live Grep** - Search text across all files.

### Features
- Fast, interactive UI for navigation.

---

## File Explorer (nerdtree)
- **Purpose**: Tree-style file explorer.

### Hotkeys
- `<Space>n`: **Toggle NERDTree** - Show/hide file explorer.

### Features
- Navigate filesystem with arrow keys or mouse.

---

## Git Integration
### vim-fugitive
- **Purpose**: Full Git workflow inside Neovim.

#### Hotkeys
- `<Space>gs`: **Git Status** - Open `:Git` status window.

#### Features
- Run Git commands (e.g., `:Git commit`, `:Git push`) directly.

### gitsigns.nvim
- **Purpose**: Git signs and hunk navigation.

#### Hotkeys (Defaults)
- `[c`: Previous hunk.
- `]c`: Next hunk.
- `<Space>hb`: **Blame** - Show line blame (toggle with `:Gitsigns toggle_current_line_blame`).

#### Features
- Signs in `signcolumn`: `+` (added), `~` (changed), `_` (deleted).

---

## Commenting (Comment.nvim)
- **Purpose**: Quick commenting/uncommenting.

### Hotkeys
- `gcc`: **Toggle Line Comment** - Comment/uncomment current line.
- `gc<motion>`: **Comment Block** - Comment a range (e.g., `gcip` for paragraph).
- `gc` (Visual mode): Comment selected lines.

### Features
- Treesitter-aware commenting for accurate syntax.

---

## Surround (nvim-surround)
- **Purpose**: Add, change, or delete surrounding pairs (e.g., quotes, brackets).

### Hotkeys
- `ys<motion><char>`: **Add Surround** - Surround motion with char (e.g., `ysiw"` adds quotes around word).
- `cs<old><new>`: **Change Surround** - Replace old with new (e.g., `cs"'` changes `"` to `'`).
- `ds<char>`: **Delete Surround** - Remove surrounding char (e.g., `ds"` removes quotes).

### Features
- Works with any pair (parentheses, tags, etc.).

---

## Multiple Cursors (vim-visual-multi)
- **Purpose**: Edit multiple locations simultaneously.

### Hotkeys
- `<Ctrl-N>`: **Start Multi-Cursor** - Select word under cursor, press again to add more occurrences.
- `<Ctrl-Down>`/`<Ctrl-Up>`: Add cursor below/above.
- `<Tab>`: Switch between cursor and selection modes.

### Features
- Type once, apply everywhere selected.

---

## Diagnostics UI (trouble.nvim)
- **Purpose**: Interactive diagnostics list.

### Hotkeys
- `<Space>t`: **Open Diagnostics** - Show all errors/warnings in a bottom window.

### Features
- Navigate diagnostics with arrow keys, open files with Enter.

---

## Debugging (nvim-dap)
- **Purpose**: Debug code with breakpoints and stepping.
- **Languages**: C/C++ (`cppdbg`), Python (`debugpy`), Rust (needs `lldb` config).

### Hotkeys
- `<Space>db`: **Toggle Breakpoint** - Add/remove breakpoint at cursor.
- `<Space>dc`: **Continue** - Start or resume debugging.

### Features
- Step through code, inspect variables (requires DAP server setup).

---

## File Marking (harpoon)
- **Purpose**: Quick navigation between marked files.

### Hotkeys
- `<Space>ha`: **Add File** - Mark current file.
- `<Space>hm`: **Toggle Menu** - Show marked files list.
- `<Space>1`: Jump to first marked file.
- `<Space>2`: Jump to second marked file.

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
- Fixed 120-column width for focused coding.

---

## Learning Tips
1. **Explore with Which-Key**: Press `<Space>` and wait to see available bindings (via `which-key.nvim`).
2. **Practice Debugging**: Set a breakpoint (`<Space>db`), start with `<Space>dc`, and use `:Dap` commands.
3. **Format on Save**: Test `conform.nvim` by editing and saving files.
4. **Multi-Cursor**: Try `<Ctrl-N>` on a repeated word, then edit all instances.
5. **Git Workflow**: Use `<Space>gs` for status, then `:Git commit`.

---

## Customization
- Adjust keybindings in `init.vim` if conflicts arise (e.g., change `<Space>t` to `<Space>d`).
- Add more DAP configs (e.g., Rust with `lldb`) as needed.
- Experiment with `mini.nvim` modules (e.g., `mini.statusline`).

Happy coding!
