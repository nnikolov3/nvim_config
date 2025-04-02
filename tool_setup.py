#!/usr/bin/env python3

# This script installs all necessary tools and dependencies for a Neovim setup on Linux,
# with additional tools for Linux kernel coding and debugging.
# It detects whether the system is Red Hat-based (e.g., Fedora, CentOS) or Debian-based (e.g., Ubuntu, Debian)
# and uses the appropriate package manager (dnf or apt) to install the tools.
# The tools include:
# - Neovim and general tools (git, curl, unzip)
# - Language servers (via mason.nvim)
# - Debuggers (via nvim-dap)
# - Formatters and linters (via conform.nvim)
# - Treesitter dependencies
# - Telescope dependencies
# - Linux kernel development tools (sparse, cscope, ctags, gdb, crash, kdump, qemu, etc.)

import os  # For interacting with the operating system (e.g., running commands, checking files)
import subprocess  # For running shell commands
import sys  # For system-specific parameters and functions (e.g., exiting the script)
import platform  # For detecting the operating system and distribution
import shutil  # For checking if commands are available
import urllib.request  # For downloading files (e.g., rustup, go, lazygit)
from pathlib import Path  # For cross-platform path handling
from textwrap import dedent  # For removing leading whitespace from multi-line strings

# --- Configuration ---
NVIM_CONFIG_DIR = Path.home() / ".config" / "nvim"  # Main Neovim config directory (~/.config/nvim)

# --- Helper Functions ---
def print_error(msg):
    """Print an error message in red to stderr."""
    print(f"\033[91mERROR: {msg}\033[0m", file=sys.stderr)

def print_success(msg):
    """Print a success message in green."""
    print(f"\033[92mSUCCESS: {msg}\033[0m")

def print_warning(msg):
    """Print a warning message in yellow."""
    print(f"\033[93mWARNING: {msg}\033[0m")

def print_info(msg):
    """Print an info message in blue."""
    print(f"\033[94mINFO: {msg}\033[0m")

def confirm(prompt):
    """
    Prompt the user for a yes/no response.
    Returns True for 'y' or 'yes', False for 'n', 'no', or empty input.
    """
    while True:
        response = input(f"{prompt} [y/N]: ").lower().strip()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no', ''):
            return False
        else:
            print("Please answer 'yes' or 'no'.")

def run_command(command, error_message=None, check=True, shell=False):
    """
    Run a shell command and handle errors.
    Args:
        command (list or str): The command to run (list for subprocess, str if shell=True).
        error_message (str, optional): Custom error message to display on failure.
        check (bool): If True, raise an exception on non-zero exit code.
        shell (bool): If True, run the command through the shell.
    Returns:
        subprocess.CompletedProcess: The result of the command execution.
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=check,
            text=True,
            capture_output=True
        )
        return result
    except subprocess.CalledProcessError as e:
        error_msg = error_message or f"Command '{' '.join(command) if isinstance(command, list) else command}' failed with exit code {e.returncode}"
        print_error(f"{error_msg}\nOutput: {e.stderr}")
        raise
    except Exception as e:
        print_error(f"Unexpected error running command '{' '.join(command) if isinstance(command, list) else command}': {e}")
        raise

def check_command_exists(command):
    """
    Check if a command is available on the system.
    Returns True if the command exists, False otherwise.
    """
    return shutil.which(command) is not None

# --- Distribution Detection ---
def detect_distribution():
    """
    Detect the Linux distribution family (Red Hat-based or Debian-based).
    Returns 'redhat' for Red Hat-based systems, 'debian' for Debian-based systems,
    or None if the distribution is not supported.
    """
    if not platform.system() == "Linux":
        print_error("This script only supports Linux systems.")
        return None

    # Check for Red Hat-based systems
    if os.path.exists("/etc/redhat-release"):
        return "redhat"
    # Check for Debian-based systems
    elif os.path.exists("/etc/debian_version"):
        return "debian"
    else:
        print_error("Unsupported Linux distribution. This script supports Red Hat-based (Fedora, CentOS) and Debian-based (Ubuntu, Debian) systems.")
        return None

# --- Installation Functions ---
def install_with_apt(packages):
    """
    Install packages using apt (Debian-based systems).
    Args:
        packages (list): List of package names to install.
    Returns:
        list: List of packages that failed to install.
    """
    print_info("Updating package lists with apt...")
    run_command(["sudo", "apt", "update"], "Failed to update package lists")

    failed_packages = []
    for package in packages:
        try:
            print_info(f"Installing package with apt: {package}")
            run_command(
                ["sudo", "apt", "install", "-y", package],
                f"Failed to install package {package} with apt"
            )
        except subprocess.CalledProcessError as e:
            print_warning(f"Failed to install {package}: {e.stderr}")
            failed_packages.append(package)

    return failed_packages

def install_with_dnf(packages):
    """
    Install packages using dnf (Red Hat-based systems).
    Args:
        packages (list): List of package names to install.
    Returns:
        list: List of packages that failed to install.
    """
    print_info("Updating package lists with dnf...")
    run_command(["sudo", "dnf", "check-update"], "Failed to update package lists", check=False)

    failed_packages = []
    for package in packages:
        try:
            print_info(f"Installing package with dnf: {package}")
            run_command(
                ["sudo", "dnf", "install", "-y", package],
                f"Failed to install package {package} with dnf"
            )
        except subprocess.CalledProcessError as e:
            print_warning(f"Failed to install {package}: {e.stderr}")
            failed_packages.append(package)

    return failed_packages

def install_rustup():
    """
    Install rustup (Rust toolchain manager) if not already installed.
    Rustup is needed for rust_analyzer, rustfmt, and nasmfmt.
    Uses urllib.request to download the installation script.
    """
    if check_command_exists("rustup"):
        print_info("rustup is already installed.")
        return

    print_info("Installing rustup...")
    # Download and run the rustup installation script
    rustup_url = "https://sh.rustup.rs"
    rustup_script = "rustup-init.sh"
    urllib.request.urlretrieve(rustup_url, rustup_script)
    run_command(
        f"sh {rustup_script} -y",
        "Failed to install rustup",
        shell=True
    )
    os.remove(rustup_script)
    # Add rustup to the PATH for the current session
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.cargo/bin")
    # Install rustfmt
    run_command(
        ["rustup", "component", "add", "rustfmt"],
        "Failed to install rustfmt"
    )

def install_go():
    """
    Install Go if not already installed.
    Go is needed for gopls, gofmt, goimports, and delve.
    Uses urllib.request to download the Go tarball.
    """
    if check_command_exists("go"):
        print_info("Go is already installed.")
        return

    print_info("Installing Go...")
    # Download the latest Go tarball (adjust version as needed)
    go_version = "1.22.2"
    go_tar = f"go{go_version}.linux-amd64.tar.gz"
    go_url = f"https://go.dev/dl/{go_tar}"
    urllib.request.urlretrieve(go_url, go_tar)
    # Extract and install Go
    run_command(
        ["sudo", "tar", "-C", "/usr/local", "-xzf", go_tar],
        "Failed to extract Go tarball"
    )
    # Remove the downloaded tarball
    os.remove(go_tar)
    # Add Go to the PATH for the current session
    os.environ["PATH"] += os.pathsep + "/usr/local/go/bin"
    # Verify installation
    if not check_command_exists("go"):
        print_error("Go installation failed.")
        sys.exit(1)

def install_lazygit():
    """
    Install lazygit if not already installed.
    Lazygit is used by toggleterm.nvim for Git integration.
    Uses urllib.request to download the lazygit tarball.
    """
    if check_command_exists("lazygit"):
        print_info("lazygit is already installed.")
        return

    print_info("Installing lazygit...")
    # Download the latest lazygit release (adjust version as needed)
    lazygit_version = "0.40.2"
    lazygit_tar = f"lazygit_{lazygit_version}_Linux_x86_64.tar.gz"
    lazygit_url = f"https://github.com/jesseduffield/lazygit/releases/download/v{lazygit_version}/{lazygit_tar}"
    urllib.request.urlretrieve(lazygit_url, lazygit_tar)
    # Extract the tarball
    run_command(
        ["tar", "-xzf", lazygit_tar],
        "Failed to extract lazygit tarball"
    )
    # Move the binary to /usr/local/bin
    run_command(
        ["sudo", "mv", "lazygit", "/usr/local/bin/"],
        "Failed to install lazygit binary"
    )
    # Remove the downloaded tarball
    os.remove(lazygit_tar)
    # Verify installation
    if not check_command_exists("lazygit"):
        print_error("lazygit installation failed.")
        sys.exit(1)

def install_golangci_lint():
    """
    Install golangci-lint if not already installed.
    golangci-lint is used by vim-go for Go linting.
    Requires Go to be installed.
    """
    if check_command_exists("golangci-lint"):
        print_info("golangci-lint is already installed.")
        return

    if not check_command_exists("go"):
        print_error("Go must be installed before installing golangci-lint.")
        sys.exit(1)

    print_info("Installing golangci-lint...")
    run_command(
        "curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.55.2",
        "Failed to install golangci-lint",
        shell=True
    )
    # Add GOPATH/bin to the PATH for the current session
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/go/bin")
    # Verify installation
    if not check_command_exists("golangci-lint"):
        print_error("golangci-lint installation failed.")
        sys.exit(1)

def install_stylua():
    """
    Install stylua using cargo (Rust package manager).
    Stylua is a Lua formatter used by conform.nvim.
    Requires rustup to be installed.
    """
    if check_command_exists("stylua"):
        print_info("stylua is already installed.")
        return

    if not check_command_exists("cargo"):
        print_error("cargo must be installed before installing stylua (run rustup installation first).")
        sys.exit(1)

    print_info("Installing stylua with cargo...")
    run_command(
        ["cargo", "install", "stylua"],
        "Failed to install stylua with cargo"
    )

def install_pip_packages(packages):
    """
    Install Python packages using pip.
    Installs into the active environment (virtual or global) without --user.
    Args:
        packages (list): List of package names to install.
    """
    if not check_command_exists("pip3"):
        print_error("pip3 must be installed before installing Python packages.")
        sys.exit(1)

    print_info(f"Installing Python packages with pip: {', '.join(packages)}")
    run_command(
        ["pip3", "install"] + packages,  # Install in the active environment
        "Failed to install Python packages with pip"
    )

def install_npm_packages(packages):
    """
    Install Node.js packages using npm.
    Args:
        packages (list): List of package names to install.
    """
    if not check_command_exists("npm"):
        print_error("npm must be installed before installing Node.js packages.")
        sys.exit(1)

    print_info(f"Installing Node.js packages with npm: {', '.join(packages)}")
    run_command(
        ["npm", "install", "-g"] + packages,
        "Failed to install Node.js packages with npm"
    )

# --- Neovim Configuration Update ---
def update_neovim_config():
    """
    Update the Neovim configuration to include plugins for Linux kernel development.
    Adds vim-linux-coding-style and cscope.nvim to the lazy.nvim setup.
    Uses dedent to format the multi-line string for the new plugins.
    """
    lazy_file = NVIM_CONFIG_DIR / "lua" / "config" / "lazy.lua"
    if not lazy_file.exists():
        print_error(f"Neovim configuration file not found: {lazy_file}")
        print_warning("Skipping Neovim configuration update.")
        return

    print_info("Updating Neovim configuration for Linux kernel development...")

    # Read the existing lazy.lua file
    with open(lazy_file, 'r') as f:
        content = f.read()

    # Find the require('lazy').setup call and add new plugins
    if "require('lazy').setup({" not in content:
        print_error("Could not find require('lazy').setup in lazy.lua")
        return

    # Define the new plugins to add
    new_plugins = dedent("""
          -- Linux kernel coding style
          {
            'vivien/vim-linux-coding-style',
            ft = {'c', 'cpp'},
            config = function()
              vim.g.linuxsty_patterns = { '/usr/src/', '/linux/' }
              print('vim-linux-coding-style configured')
            end,
          },
          -- Cscope integration for code navigation
          {
            'dhananjaylatkar/cscope.nvim',
            dependencies = { 'nvim-telescope/telescope.nvim' },
            ft = {'c', 'cpp'},
            config = function()
              require('cscope').setup({
                db_file = './cscope.out', -- Location of cscope database
                cscope = {
                  exec = 'cscope', -- Cscope executable
                  picker = 'telescope', -- Use Telescope for results
                },
              })
              -- Keymaps for cscope
              local map = vim.keymap.set
              map('n', '<leader>cs', ':Cs find s <C-R>=expand("<cword>")<CR><CR>', { desc = 'Cscope find symbol' })
              map('n', '<leader>cg', ':Cs find g <C-R>=expand("<cword>")<CR><CR>', { desc = 'Cscope find definition' })
              map('n', '<leader>cc', ':Cs find c <C-R>=expand("<cword>")<CR><CR>', { desc = 'Cscope find callers' })
              print('cscope.nvim configured')
            end,
          },
    """)

    # Insert the new plugins into the require('lazy').setup table
    # Find the first plugin entry and insert after it
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("{"):
            # Insert the new plugins after the first plugin entry
            lines.insert(i + 1, new_plugins)
            break

    # Write the updated content back to lazy.lua
    updated_content = "\n".join(lines)
    with open(lazy_file, 'w') as f:
        f.write(updated_content)

    print_success("Neovim configuration updated with Linux kernel plugins.")

# --- Main Installation Function ---
def install_tools():
    """
    Main function to install all tools required for the Neovim setup,
    including tools for Linux kernel coding and debugging.
    Detects the distribution and installs tools accordingly.
    """
    # Detect the Linux distribution
    distro = detect_distribution()
    if not distro:
        sys.exit(1)

    # Define the packages to install based on the distribution
    if distro == "redhat":
        package_manager = "dnf"
        packages = [
            "neovim",  # Neovim editor
            "git",  # For cloning plugins
            "curl",  # For downloading files
            "unzip",  # For extracting archives (used by Mason)
            "nodejs",  # For JavaScript/TypeScript LSP and tools
            "npm",  # Node package manager
            "python3",  # For Python LSP and debugging
            "python3-pip",  # Python package manager
            "gcc",  # For compiling Treesitter parsers and kernel modules
            "make",  # For building tools like telescope-fzf-native
            "ripgrep",  # For Telescope live_grep
            "fd-find",  # For Telescope find_files (called fdfind on Red Hat)
            "clang",  # For clangd (C/C++ LSP) and clang-format
            "bash",  # For bashls (usually pre-installed)
            "shfmt",  # For shell script formatting
            # Linux kernel development tools
            "sparse",  # Static analysis tool for the Linux kernel
            "cscope",  # For code navigation
            "ctags",  # For tag generation (exuberant-ctags on Fedora)
            "gdb",  # For debugging kernel modules and user-space programs
            "crash",  # For analyzing kernel crash dumps
            "qemu-system-x86",  # For running a virtual machine to test the kernel
            "strace",  # For tracing system calls
            "ltrace",  # For tracing library calls
            f"kernel-devel-{platform.release()}",  # Kernel headers for the current kernel
            "ncurses-devel",  # For menuconfig
        ]
    else:  # Debian-based
        package_manager = "apt"
        packages = [
            "neovim",  # Neovim editor
            "git",  # For cloning plugins
            "curl",  # For downloading files
            "unzip",  # For extracting archives (used by Mason)
            "nodejs",  # For JavaScript/TypeScript LSP and tools
            "npm",  # Node package manager
            "python3",  # For Python LSP and debugging
            "python3-pip",  # Python package manager
            "build-essential",  # Includes gcc, g++, make for compiling Treesitter parsers
            "ripgrep",  # For Telescope live_grep
            "fd-find",  # For Telescope find_files (called fd on Debian)
            "clangd",  # For C/C++ LSP
            "clang-format",  # For C/C++ formatting
            "bash",  # For bashls (usually pre-installed)
            "shfmt",  # For shell script formatting
            # Linux kernel development tools
            "sparse",  # Static analysis tool for the Linux kernel
            "cscope",  # For code navigation
            "ctags-universal",  # For tag generation (universal-ctags on Debian)
            "gdb",  # For debugging kernel modules and user-space programs
            "crash",  # For analyzing kernel crash dumps
            "kdump-tools",  # For capturing kernel crash dumps
            "kexec-tools",  # For kdump
            "qemu-system-x86",  # For running a virtual machine to test the kernel
            "strace",  # For tracing system calls
            "ltrace",  # For tracing library calls
            f"linux-headers-{platform.release()}",  # Kernel headers for the current kernel
            "libncurses-dev",  # For menuconfig
        ]

    # Prompt the user to confirm installation
    if not confirm(f"Install Neovim and required tools using {package_manager} ({', '.join(packages)})?"):
        print_warning("Installation aborted by user.")
        sys.exit(0)

    # Install packages using the appropriate package manager
    try:
        if distro == "redhat":
            failed_packages = install_with_dnf(packages)
        else:
            failed_packages = install_with_apt(packages)
        if failed_packages:
            print_warning(f"The following packages failed to install: {', '.join(failed_packages)}")
    except Exception as e:
        print_error(f"Failed to install packages: {e}")
        sys.exit(1)

    # Install additional tools that require special handling
    try:
        # Install rustup for Rust tools
        install_rustup()
        # Install Go for Go tools
        install_go()
        # Install lazygit for Git integration
        install_lazygit()
        # Install golangci-lint for Go linting
        install_golangci_lint()
        # Install stylua with cargo
        install_stylua()
        # Install Python packages
        install_pip_packages(["black", "isort"])
        # Install Node.js packages (removed stylua)
        install_npm_packages(["prettier"])
    except Exception as e:
        print_error(f"Failed to install additional tools: {e}")
        sys.exit(1)

    # Update Neovim configuration with Linux kernel plugins
    try:
        update_neovim_config()
    except Exception as e:
        print_error(f"Failed to update Neovim configuration: {e}")
        print_warning("You may need to manually add the Linux kernel plugins to your configuration.")

    # Verify installations
    print_info("Verifying installations...")
    tools_to_verify = [
        "nvim", "git", "curl", "unzip", "node", "npm", "python3", "pip3",
        "gcc", "make", "rg", "fd", "clang", "bash", "shfmt", "rustup",
        "go", "lazygit", "golangci-lint", "black", "isort", "prettier", "stylua",
        # Linux kernel tools
        "sparse", "cscope", "ctags", "gdb", "crash",
        "qemu-system-x86_64", "strace", "ltrace"
    ]
    missing_tools = []
    for tool in tools_to_verify:
        if not check_command_exists(tool):
            missing_tools.append(tool)
            print_warning(f"{tool} is not installed or not in PATH.")
        else:
            print_success(f"{tool} is installed.")

    if missing_tools:
        print_error(f"The following tools are missing: {', '.join(missing_tools)}")
        print_warning("Some Neovim plugins or kernel development features may not work correctly without these tools.")
    else:
        print_success("All tools are installed successfully!")

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Neovim Tools Installation for Linux ---")
    print(f"System: {platform.system()} {platform.release()}")
    print("-" * 40)

    # Check if the script is running with sufficient privileges
    if os.geteuid() != 0:
        print_warning("This script may require sudo privileges to install packages.")
        print_info("You may be prompted for your sudo password during installation.")

    # Run the installation process
    install_tools()

    print("-" * 40)
    print_success("Neovim tools installation complete!")
    print("\nNext Steps:")
    print("1. Launch Neovim (`nvim`) and let lazy.nvim install the new plugins.")
    print("2. Run `:checkhealth` in Neovim to diagnose any issues.")
    print("3. Run `:Mason` to verify LSP installations.")
    print("4. For Linux kernel development:")
    print("   - Navigate to your kernel source directory (e.g., /usr/src/linux).")
    print("   - Generate cscope database: `cscope -R -b -q`")
    print("   - Use `<leader>cs` to find symbols, `<leader>cg` to find definitions.")
    print("   - Use `gdb` for debugging (configure nvim-dap if needed).")
    print("   - Use `sparse` for static analysis: `make C=1 CHECK=sparse`")
    print("--- Enjoy your enhanced Neovim setup for Linux kernel development! ---")
