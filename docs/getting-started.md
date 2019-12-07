Getting XQEMU
-------------
**Download for Windows:** The latest, pre-built release version of XQEMU for Windows can be [**downloaded here**](https://ci.appveyor.com/api/projects/xqemu-bot/xqemu/artifacts/xqemu.zip?branch=master&job=Environment:%20MSYS2_ARCH=x86_64,%20MSYSTEM=MINGW64;%20Configuration:%20Release&pr=false).

Linux and macOS users will need to build XQEMU from source, see [Building XQEMU from Source](developers/building.md).

Required Files
--------------
XQEMU is a low-level, full-system emulator which emulates the actual hardware of
the Xbox; this means that in order to actually run XQEMU, you must have a copy
of the stuff that a real Xbox needs when it turns on:

1. The MCPX Boot ROM image
2. The flash ROM image (aka *BIOS*)
3. A properly-formatted hard disk drive image
4. Game disc image(s)

Unfortunately, distributing some of these items would violate copyright laws, so
you'll need to acquire them on your own.


#### Flash ROM Image (aka BIOS/Kernel)

Xbox 1.0 compatible BIOS (cromwell, 4034, 4036, ...). You can use a retail
or debug image. Just like a real Xbox, running an unmodified retail BIOS will
not allow booting unofficial software.

People have reported most success using the modified "COMPLEX 4627" BIOS (retail version).



Running XQEMU
-------------

XQEMU is launchable via the command-line interface, or through the [XQEMU-Manager
GUI](https://github.com/xqemu/xqemu-manager).

### Using XQEMU-Manager

XQEMU-Manager is a simple application with a graphical interface that allows you
to easily configure, launch, and control XQEMU. Currently it is distributed separately
from the main XQEMU executable. A binary distribution of XQEMU-Manager for Windows
is [available here](https://ci.appveyor.com/api/projects/xqemu-bot/xqemu-manager/artifacts/xqemu-manager.zip?branch=master&pr=false).

Upon starting XQEMU-Manager, you will be presented with the following interface:

![XQEMU-Manager Main Window](xqemu-manager-main.png)

You will need to edit your configuration to let XQEMU-Manager know where XQEMU
is located, and where to find the files described above. Navigate to
<kbd>Edit</kbd>&rarr;<kbd>Settings</kbd> and you will be presented with the
following dialog:

![XQEMU-Manager Settings Window](xqemu-manager-settings.png)

After configuring your settings, close the settings dialog and click the
<kbd>Start</kbd> button to launch XQEMU.

### Using the Command-Line Interface

You can launch with the following command:

    ./i386-softmmu/qemu-system-i386 \
        -cpu pentium3 \
        -machine xbox,bootrom=$MCPX \
        -m 64 \
        -bios $BIOS \
        -drive index=0,media=disk,file=$HDD,locked \
        -drive index=1,media=cdrom,file=$DISC \
        -usb -device usb-xbox-gamepad

Of course, on Windows the executable path will have a `.exe` extension. If launching
a pre-built binary from AppVeyor, replace `./i386-softmmu/qemu-system-i386` with
`xqemu.exe`.

Replace the variables `$MCPX`, `$BIOS`, `$HDD`, and `$DISC` with the appropriate
file paths or define them as variables in your shell.

The Xbox boot animation sequence can be bypassed by adding the
`,short-animation` option to the `-machine` switch above.
