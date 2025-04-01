# Neovim Hotkeys and Functionality Guide

This guide covers the keybindings and features of your Neovim setup as of your latest `init.vim`. It includes plugins for LSP, formatting, debugging, navigation, Git integration, testing, autosave, buffer management, session persistence, and more. Your leader key is `<Space>` (set with `let mapleader = " "`).

---

## General Neovim Hotkeys
- `<C-a>`: **Select All** - Visually select entire buffer (`ggVG`).
- `:w`: Save file (rarely needed due to autosave).
- `:q`: Quit (prompts confirmation if unsaved changes exist).
- `/<pattern>`: Search (with `hlsearch` and `incsearch` enabled).
- `n`/`N`: Next/previous search match.

---

## LSP (nvim-lspconfig + rust-tools.nvim)
- **Purpose**: Language server support for code navigation, diagnostics, completion, and Rust-specific enhancements.
- **Languages**: C/C++ (`clangd`), Rust (`rust-analyzer` via `rust-tools`), Python (`pyright`).

### Hotkeys
- `gd`: **Go to Definition** - Jump to symbol definition.
- `K`: **Hover** - Show documentation or type info under cursor.
- `<Space>rn`: **Rename** - Rename symbol across project.
- `<Space>ca`: **Code Action** - Trigger fixes or refactorings (e.g., Rust imports).
- `[d`: **Previous Diagnostic** - Jump to previous error/warning.
- `]d`: **Next Diagnostic** - Jump to next error/warning.

### Features
- Inline diagnostics shown via `virtual_text` and `signcolumn`.
- LSP progress displayed in statusline (via `lualine-lsp-progress`).
- Rust-specific features from `rust-tools.nvim`: inlay hints, advanced code actions, and tighter `rust-analyzer` integration.

---

## Autocompletion (nvim-cmp)
- **Purpose**: LSP-driven autocompletion.

### Hotkeys
- `<CR>` (Enter): Confirm selected completion.
- `<C-n>`: Next completion item.
- `<C-p>`: Previous completion item.

### Features
- Autocompletion triggered as you type, powered by LSP sources (enhanced for Rust via `rust-tools`).

---

## Autosave (auto-save.nvim)
- **Purpose**: Automatically save changes to avoid data loss.

### Features
- Saves on `InsertLeave` and `TextChanged` events.
- 135ms debounce delay to prevent excessive writes.
- Displays "AutoSave: saved at HH:MM:SS" in statusline.

---

## Formatting (conform.nvim)
- **Purpose**: Auto-format code on save using external tools.
- **Tools**: `clang-format` (C/C++), `rustfmt` (Rust), `black` (Python).

### Features
- Formats on save with 500ms timeout.
- Falls back to LSP formatting if the tool fails.
- Error notifications enabled.

---

## File Navigation (telescope.nvim)
- **Purpose**: Fuzzy finding for files, text, and projects.

### Hotkeys
- `<Space>ff`: **Find Files** - Search and open files in current directory.
- `<Space>fg`: **Live Grep** - Search text across all files.
- `<Space>fp`: **Find Projects** - List and switch between projects (via `project.nvim`).

### Features
- Fast, interactive UI with Telescope integration.
- Project-aware navigation (via `project.nvim`).

---

## File Explorer (nvim-tree.lua)
- **Purpose**: Modern tree-style file explorer.

### Hotkeys
- `<Space>n`: **Toggle NvimTree** - Show/hide file explorer.

### Features
- Navigate with arrow keys or mouse.
- Git status integration for files.

---

## Buffer Management (bufferline.nvim)
- **Purpose**: Visual buffer tabs with diagnostics.

### Hotkeys
- `<Space>b`: **Pick Buffer** - Select a buffer from the tabline.

### Features
- Shows LSP diagnostics in tabs.
- Offsets for NvimTree integration.

---

## Session Management (persistence.nvim)
- **Purpose**: Save and restore editing sessions.

### Hotkeys
- `<Space>ss`: **Restore Session** - Load session for current directory.
- `<Space>sl`: **Restore Last Session** - Load most recent session.

### Features
- Saves buffers, cursor positions, tabs, and window sizes.
- Stores sessions in `~/.local/state/nvim/sessions/`.

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
- `<Space>hb`: **Blame** - Toggle line blame (via `:Gitsigns toggle_current_line_blame`).

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
- Treesitter-aware commenting for accurate syntax (supports TOML, Rust, etc.).

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
- `<Space>t`: **Open Diagnostics** - Show all errors/warnings in a bottom window.

### Features
- Navigate diagnostics with arrow keys, open files with Enter.

---

## Debugging (nvim-dap)
- **Purpose**: Debug code with breakpoints and stepping.
- **Languages**: C/C++ (`cppdbg`), Python (`debugpy`), Rust (`lldb`).

### Hotkeys
- `<Space>db`: **Toggle Breakpoint** - Add/remove breakpoint at cursor.
- `<Space>dc`: **Continue** - Start or resume debugging.

### Features
- Step through code, inspect variables.
- Rust debugging via LLDB (configure path to `lldb-vscode` in `init.vim`).

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

## Testing (vim-test)
- **Purpose**: Run tests directly from Neovim.
- **Frameworks**: pytest (Python), Cargo (Rust), Google Test (C++).

### Hotkeys
- `<Space>tn`: **Test Nearest** - Run test under cursor.
- `<Space>tf`: **Test File** - Run all tests in current file.
- `<Space>ts`: **Test Suite** - Run entire test suite.

### Features
- Runs in Neovim terminal (via `test#strategy = "neovim"`).

---

## Project Management (project.nvim)
- **Purpose**: Detect and manage projects, integrate with Telescope.

### Hotkeys
- `<Space>fp`: **Find Projects** - List and switch between projects.

### Features
- Auto-detects projects via LSP or patterns (e.g., `.git`, `Cargo.toml`).

---

## Fast Navigation (leap.nvim)
- **Purpose**: Jump to any visible location with minimal keystrokes.

### Hotkeys
- `z<char><char>`: **Jump Forward** - Jump to first occurrence of two characters (e.g., `zab` jumps to "ab").
- `Z<char><char>`: **Jump Backward** - Jump to previous occurrence.

### Features
- Works in normal, visual, and operator-pending modes.
- Highlights jump targets for selection.

---

## Syntax Highlighting (nvim-treesitter)
- **Purpose**: Advanced syntax highlighting and parsing.
- **Languages**: C, C++, Rust, Python, TOML.

### Features
- Precise highlighting for code and config files (e.g., `Cargo.toml`).
- Powers plugins like `Comment.nvim` for context-aware commenting.

---

## Learning Tips
1. **Explore with Which-Key**: Press `<Space>` and wait to see available bindings (via `which-key.nvim`).
2. **Leverage Autosave**: Edit freely; `auto-save.nvim` handles saving (check statusline for confirmation).
3. **Manage Buffers**: Use `<Space>b` to switch buffers visually with `bufferline.nvim`.
4. **Restore Sessions**: Use `<Space>ss` or `<Space>sl` to pick up where you left off.
5. **Practice Debugging**: Set a breakpoint (`<Space>db`), start with `<Space>dc`, explore `:Dap` commands (try Rust with LLDB).
6. **Format on Save**: Test `conform.nvim` by editing and saving files (e.g., Rust with `rustfmt`).
7. **Multi-Cursor**: Try `<Ctrl-N>` on a repeated word, then edit all instances.
8. **Git Workflow**: Use `<Space>gs` for status, then `:Git commit`.
9. **Rust Tools**: Hover (`K`) over Rust code to see inlay hints or type info (via `rust-tools`).

---

## Customization
- Adjust keybindings in `init.vim` if conflicts arise (e.g., change `<Space>t` to `<Space>d`).
- Update DAP paths (e.g., Rust’s `lldb-vscode` location) in the `nvim-dap` section.
- Experiment with `mini.nvim` modules (e.g., `mini.statusline`).
- Remove legacy `NERDTree` (`Plug 'preservim/nerdtree'`) since `nvim-tree.lua` is active.
