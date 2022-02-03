gif2tgsticker
====================

Tool for converting gif to Telegram Sticker(webm)

Introduction
--------------------

Telegram added [Video Sticker Support](https://core.telegram.org/stickers#video-sticker-requirements), This tool tries to:

* Convert video to WebM
* Resize video within 512px and keeping aspect ratio
* Speed up video if it's longer than 3 seconds

This tool also supports non-GIF files(mp4, apng...) despite its name, but it's optimized for converting small-short videos.

How to use
--------------------

### Windows

Download [gif2tgsticker.exe from releases](../../releases) and put together with [FFmpeg](https://www.ffmpeg.org/download.html) files.


### Other platform

```
poetry install
poetry run python gif2tgsticker.py
```


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
