import os
from pathlib import Path
from pprint import pprint
import tkinter as tk
import subprocess

import ffmpeg

import tkinterdnd2 as tkd

DEFAULT_FPS = 30
DEFAULT_SMART_DURATION_LIMIT = '2.9'
DEFAULT_RESIZE_MODE = 'scale'
DEFAULT_SPEED_ADJUST_MODE = 'smart'
DEFAULT_FALLBACK_PTS = '1.0'
DEFAULT_CRF = -1
DEFAULT_APNG_DELAY = "-1"

root = tkd.TkinterDnD.Tk()
root.withdraw()
root.title('gif2tgsticker')
root.grid_columnconfigure(0, minsize=600)

fps_var = tk.IntVar()
fps_var.set(DEFAULT_FPS)

speed_adjust_mode_var = tk.StringVar()
speed_adjust_mode_var.set(DEFAULT_SPEED_ADJUST_MODE)

smart_limit_duration_var = tk.StringVar()
smart_limit_duration_var.set(DEFAULT_SMART_DURATION_LIMIT)

fallback_pts_var = tk.StringVar()
fallback_pts_var.set(DEFAULT_FALLBACK_PTS)

resize_mode_var = tk.StringVar()
resize_mode_var.set(DEFAULT_RESIZE_MODE)

crf_var = tk.IntVar()
crf_var.set(DEFAULT_CRF)

apng_delay_var = tk.StringVar()
apng_delay_var.set(DEFAULT_APNG_DELAY)

option_box = tk.Frame(root)
option_box.grid(row=0, column=0)

row = 0

tk.Label(option_box, text="FPS:")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=fps_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(option_box, text="Resize mode:")\
  .grid(row=row, column=0)

radio_box = tk.Frame(option_box)
radio_box.grid(row=row, column=1)

tk.Radiobutton(radio_box, text='Scale', value='scale', variable=resize_mode_var)\
  .grid(row=0, column=0)
tk.Radiobutton(radio_box, text='Pad', value='pad', variable=resize_mode_var)\
  .grid(row=0, column=1)

row += 1

tk.Label(option_box, text="Smart speed adjust duration limit\n(when video is longer than 3 seconds):")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=smart_limit_duration_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(option_box, text="Smart speed adjust fallback PTS modifier\n(Used when unable to get duration from video)\n(0.5 = 2x speed):")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=fallback_pts_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(option_box, text="CRF Value(0-51, higher means lower quality, -1=unset):")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=crf_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(option_box, text="WebP to APNG delay(lower means faster playback, -1=unset):")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=apng_delay_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(root, text='Drag and drop files here:')\
  .grid(row=row, column=0, padx=10, pady=5)

row += 1

listbox = tk.Listbox(root, width=1, height=20)
listbox.grid(row=row, column=0, padx=5, pady=5, sticky='news')


row += 1

def drop(event):
    if event.data:
        print('Dropped data:\n', event.data)

        if event.widget == listbox:
            # event.data is a list of filenames as one string;
            # if one of these filenames contains whitespace characters
            # it is rather difficult to reliably tell where one filename
            # ends and the next begins; the best bet appears to be
            # to count on tkdnd's and tkinter's internal magic to handle
            # such cases correctly; the following seems to work well
            # at least with Windows and Gtk/X11
            files = listbox.tk.splitlist(event.data)

            for f in files:
                if os.path.exists(f):
                    process_file(f)
                    print('Dropped file: "%s"' % f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f)

    return event.action


def convert_webp_to_apng(filepath: str):
    print("Converting WebP to APNG...")

    p = Path(filepath)
    output_path = p.with_suffix(".png")
    subprocess.run(["magick",
                    *([] if apng_delay_var.get() == "-1" else ["-delay",  apng_delay_var.get()]),
                    filepath,
                    "apng:" + str(output_path)
                   ])
    return str(output_path.absolute())

def process_file(filepath):
    if filepath.lower().endswith(".webp"):
        filepath = convert_webp_to_apng(filepath)

    p = Path(filepath)

    job = ffmpeg.input(filepath)

    # 30FPS
    job = job.filter('fps', fps=fps_var.get())

    info = ffmpeg.probe(filepath)

    pprint(info)

    stream = info['streams'][0]
    fmt = info['format']

    if resize_mode_var.get() == 'scale':
        # Try to scale to 512px
        if stream['width'] >= stream['height']:
            job = job.filter('scale', 512, -1)
        else:
            job = job.filter('scale', -1, 512)

    elif resize_mode_var.get() == 'pad':
        if stream['width'] >= stream['height']:
            job = job.filter('pad', width=512, height='min(ih,512)', x='(ow-iw)/2', y='(oh-ih)/2', color="white@0")
        else:
            job = job.filter('pad', width='min(iw,512)', height=512, x='(ow-iw)/2', y='(oh-ih)/2', color="white@0")


    if 'duration' in fmt:
        print("Duration detected: %s" % fmt['duration'])
        duration = float(fmt['duration'])

        # Try speed up video if it's over 3 seconds
        if duration > 3.0:
            job = job.filter('setpts', f"({smart_limit_duration_var.get()}/{duration})*PTS")
    else:
        print("Unable to determine duration")
        job = job.filter('setpts', f"{fallback_pts_var.get()}*PTS")


    out_path = str(p.with_suffix('.webm'))

    if os.path.exists(out_path):
        out_path = str(p.with_suffix('.telegram.webm'))

    extra_args = {}

    if crf_var.get() != -1:
      extra_args['crf'] = crf_var.get()

    job = (
        job
        .output(
            out_path,
            pix_fmt='yuva420p',
            vcodec='libvpx-vp9',
            an=None,  # Remove Audio
            **extra_args,
        )
        .overwrite_output()
    )

    job.run()

    listbox.insert(0, out_path)

listbox.drop_target_register(tkd.DND_FILES, tkd.DND_ALL)
listbox.dnd_bind('<<Drop>>', drop)

root.update_idletasks()
root.deiconify()
root.mainloop()
