gif2tgsticker
====================

Tool for converting gif to WebM video for [Telegram Video Sticker](https://core.telegram.org/stickers#video-sticker-requirements)

This tool also supports non-GIF files(mp4, apng...) despite its name, but it's optimized for converting small-short videos.

How to use
--------------------

### Windows

Install [ImageMagick](https://imagemagick.org/script/download.php#windows), make sure "Install FFmpeg" option is checked.

Download [gif2tgsticker.exe from releases](../../releases).


### Other platform

Install ffmpeg, ImageMagick(for WebP to GIF Conversion)

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

### CRF Value

You can adjust quality of result with this value. Try changing when size of result is >= 256kb

[Read FFmpeg document](https://trac.ffmpeg.org/wiki/Encode/H.264) for more information.


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
