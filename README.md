# bikeopticon
Automate processing of helmet or dash camera footage

Helmet cameras are used by many cyclists, motorcycle riders, and drivers for protection on the roadways. Often, footage is worth saving because it demonstrates poor behavior by other road users, including harassment - many users like to review the footage en-masse when they have free time. However, managing the footage can be time-consuming or annoying, particularly given the volume of footage (5 minutes can be nearly 1GB) relative to microSD and USB2 transfer speeds.

For users who mount their camera on a helmet, the camera has to be charged regularly via USB anyway; charging current requirements often are at or below standard USB current limits. Inexpensive SBCs like the Raspberry Pi lend themselves well to automating some of the process, have enough ports for 2 cameras plus mass storage, and being located near where one would store their helmet for convenience. Connect the camera when you return from a journey, and the SBC transfers files off, files them, applies stabilization, transcodes them to a format friendly for youtube, etc.

This is not (presently) intended for use on a multi-user, untrusted systems, etc.

## Todos / goals

* Given a filename, run video stabilization analysis, then transcode to youtube-friendly format.
* Command line switch to strip audio tracks from final file
* Command line switch to crop frame to remove times/location/speed stamps from final file


* Add directory processing
* Be cron-friendly
* Provide option to do something with locked files (many cameras can lock the current file when a button is pushed during recording, or do so when there is an impact/shock.)

* Add directory watching (PyInotify or similar)

* Alert the user when videos have invalid dates or are unexpected dimensions (some cameras lose their date/time and other settings)
* Drive a multicolor LED to indicate status

* 3D printed case for an SBC with bicycle helmet hook and mount for attaching to a bicycle rack