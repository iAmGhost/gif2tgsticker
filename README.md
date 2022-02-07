gif2tgsticker
====================

Tool for converting gif to WebM video for [Telegram Video Sticker](https://core.telegram.org/stickers#video-sticker-requirements)

How to use
--------------------

### Windows

Download [gif2tgsticker.exe from releases](../../releases) and put together with [FFmpeg](https://www.ffmpeg.org/download.html) files.


### Other platform

```
poetry install
poetry run python gif2tgsticker.py
```

Options
--------------------

### FPS

Telegram supports up to 30 FPS.

Note that Video Stickers have 256KB file size limit, lowering framerate can help for fitting.

### Resize mode

Since Telegram requires video to have 512px on one side, it tries to adjust it.

  * Scale: Scale up/down image itself.
    * Landscape video will have 512px width, height will be resized within aspect ratio.
    * Vertical video will have 512px height, width will be resized within aspect ratio.
  * Pad: Add transparent padding
    * Landscape video will have left, right padding.
    * Vertical video will have top, bottom padding.


### Smart speed adjust duration limit

Telegram Video Sticker have 3 seconds duration limit.

If the video is longer than 3 seconds, this tool will try to fit this duration by speeding up playback.


### Smart speed adjust fallback PTS modifier

If this tool is unable to get playback duration from file, this value will be used as PTS(Presentation Time Stamp) modifier.

* 1.0 means 1x playback speed
* 0.5 means 2x playback speed


Dependencies
--------------------

* [FFmpeg](https://www.ffmpeg.org/)
* [Poetry](https://python-poetry.org/)
* tkinterdnd2
* ffmpeg-python


Packaging
------------------

```
poetry install
poetry shell
pyinstaller gif2tgsticker.spec
```
