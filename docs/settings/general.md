## XQEMU

### XQEMU Executable

This is the XQEMU main exectuable (typically xqemu.exe or qemu-system-i386.exe) that will be started.

### Use hardware acceleration

!!! attention
	This should remain disabled, unless you know what you are doing.

This option will enable hardware acceleration using one of the following drivers:

- KVM (Intel / AMD CPUs on Linux)
- HAXM (Intel CPUs on Windows, macOS and Linux)
- WHPX (Intel / AMD CPUs on Windows)

The support for some CPU models is also really bad.
We therefore generally advise to disable this option.

All of these solutions also sacrifice emulation quality for a slight increase in speed.
Results will differ per game.


## Boot options

### Use short boot animation sequence

This is a hack which makes the Xbox think that it is rebooting instead of starting from a cold-boot.
This skips the long boot animation sequence.
The Xbox logo will still be shown.


## DVD Drive

### Disc Present

This will enable emulation of a disc in the DVD drive.

### Disc Image

Path to the file that is used for the disc that is in the DVD drive.
