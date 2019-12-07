
## Firmware

XQEMU behaves like a virtual original Xbox 1.0.
It currently does not support images of later Xbox models.

!!! attention

		The XQEMU project does not endorse or promote piracy. We don't link to
		copyrighted files, or discuss how to acquire them. The only legal way to
		acquire these files is to dump them from *your real, physical Xbox*. Please
		don't ask us how to get them.


#### MCPX ROM Image

There were 2 different versions of the Xbox MCPX ROM.
XQEMU has better support for MCPX 1.0 than for MCPX 1.1.

		MD5 (mcpx_1.0.bin) = d49c52a4102f6df7bcf8d0617ac475ed

If your MCPX dump has an MD5 of `196a5f59a13382c185636e691d6c323d`, you dumped
it badly and it's a couple of bytes off. It should start with `0x33 0xC0` and end
with `0x02 0xEE`.

#### Flash Image

The Flash contains the bios / kernel.
The bios will be started by code in the MCPX ROM.
Therefore your Flash Image must be compatible with the chosen MCPX ROM image.

!!! important
	The earliest Xbox kernel, version 3944, has a known problem with the input emulation in XQEMU.
	It will not accept input in XQEMU.

!!! important
	XQEMU currently doesn't emulate DVD security checks.
	The kernel should be patched, so it doesn't do those security checks.
	If this isn't done, it will refuse to read any disc.
	
	You can either patch the kernel using a modified flash image, or by installing a softmod in your virtual Xbox.


## Hard Disk

### HDD Image

You have options:

#### Option 1: Use a pre-built Xbox HDD image (recommended)

You can use a pre-built 8G Xbox HDD image, free of any copyrighted content, and
only containing a dummy dashboard. [You can download this image from
here!](https://github.com/xqemu/xqemu-hdd-image/releases)

!!! note

	By design, this particular drive image does not contain the official Xbox
	dashboard, but instead contains only a dummy dashboard. Because of this, you
	may see an error message when starting XQEMU with an unmodified retail BIOS
	image due to the system failing to find a properly signed dashboard.

	If you would like to change your dashboard (perhaps to the official retail
	dashboard, or any alternative dashboard), or copy additional files over to
	the Xbox HDD, you can start XQEMU, using a modified BIOS image, and a disc
	containing an alternative dashboard. Then you can either install that
	dashboard, or connect to XQEMU using FTP to transfer your desired dashboard
	files to the HDD.

#### Option 2: Image your real Xbox HDD

This is the most authentic way to do it. Unlock your drive, connect it to a
computer, and `dd` the entire contents of the drive straight to a file. This
file can be used as-is with XQEMU.

#### Option 3: Build a new HDD image from scratch

You can also create an Xbox hard-disk image using XboxHDM. Directions on how
to do this [can be found here](https://github.com/xqemu/xqemu-hdd-image).
- Use our dummy HDD image (<﻿https://github.com/xqemu/xqemu-hdd-image/releases﻿>)

### Locked

The original Xbox locks the Hard Disk with a key stored in the EEPROM.
XQEMU can pretend that the Hard Disk was locked as the Kernel will check for it.

This should typically be enabled.


## Memory

### Installed System Memory

The amount of memory the virtual Xbox will use.

This should typically be 64 MiB for a retail Xbox.

Development kits of the original Xbox have 128 MiB.
