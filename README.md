# StellarSynthCompiler
BSCS 3rd Year Students' C++ and Python Compiler. By Travellers' Syndicate. StellarSynth Compiler

Customtkinter:
https://customtkinter.tomschimansky.com/

GCC Compiler:
Installing the MinGW-w64 toolchain
Get the latest version of MinGW-w64 via MSYS2, which provides up-to-date native builds of GCC, MinGW-w64, and other helpful C++ tools and libraries. This will provide you with the necessary tools to compile your code, debug it, and configure it to work with IntelliSense.

To install the MinGW-w64 toolchain, check out this video or follow the steps below:


You can download the latest installer from the MSYS2 page or use this direct link to the installer.

Run the installer and follow the steps of the installation wizard. Note that MSYS2 requires 64 bit Windows 8.1 or newer.

In the wizard, choose your desired Installation Folder. Record this directory for later. In most cases, the recommended directory is acceptable. The same applies when you get to setting the start menu shortcuts step. When complete, ensure the Run MSYS2 now box is checked and select Finish. This will open a MSYS2 terminal window for you.

In this terminal, install the MinGW-w64 toolchain by running the following command:

pacman -S --needed base-devel mingw-w64-ucrt-x86_64-toolchain
Accept the default number of packages in the toolchain group by pressing Enter.

MYSS2 Installer

Enter Y when prompted whether to proceed with the installation.

Add the path to your MinGW-w64 bin folder to the Windows PATH environment variable by using the following steps:

In the Windows search bar, type Settings to open your Windows Settings.
Search for Edit environment variables for your account.
In your User variables, select the Path variable and then select Edit.
Select New and add the MinGW-w64 destination folder you recorded during the installation process to the list. If you used the default settings above, then this will be the path: C:\msys64\ucrt64\bin.
Select OK to save the updated PATH. You will need to reopen any console windows for the new PATH location to be available.
Check your MinGW installation
To check that your MinGW-w64 tools are correctly installed and available, open a new Command Prompt and type:

gcc --version
g++ --version
gdb --version
You should see output that states which versions of GCC, g++ and GDB you have installed. If this is not the case:

Make sure your PATH variable entry matches the MinGW-w64 binary location where the toolchain was installed. If the compilers do not exist at that PATH entry, make sure you followed the previous instructions.
If gcc has the correct output but not gdb, then you need to install the packages you are missing from the MinGW-w64 toolset.
If on compilation you are getting the "The value of miDebuggerPath is invalid." message, one cause can be you are missing the mingw-w64-gdb package.
