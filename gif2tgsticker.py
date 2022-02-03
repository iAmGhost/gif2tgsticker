import os
from pathlib import Path
from pprint import pprint
import tkinter as tk

import ffmpeg

import tkinterdnd2 as tkd

DEFAULT_FPS = 30
DEFAULT_DURATION_LIMIT = 175

root = tkd.TkinterDnD.Tk()
root.withdraw()
root.title('gif2tgsticker')
root.grid_columnconfigure(0, minsize=600)

fps_var = tk.IntVar()
fps_var.set(DEFAULT_FPS)

limit_duration_var = tk.IntVar()
limit_duration_var.set(DEFAULT_DURATION_LIMIT)

option_box = tk.Frame(root)
option_box.grid(row=0, column=0)

tk.Label(option_box, text="FPS:")\
  .grid(row=0, column=0)
tk.Entry(option_box, textvariable=fps_var)\
  .grid(row=0, column=1)

tk.Label(option_box, text="Limit duration to(if over 3 seconds):")\
  .grid(row=1, column=0)
tk.Entry(option_box, textvariable=limit_duration_var)\
  .grid(row=1, column=1)

tk.Label(root, text='Drag and drop files here:')\
  .grid(row=1, column=0, padx=10, pady=5)


listbox = tk.Listbox(root, width=1, height=20)
listbox.grid(row=2, column=0, padx=5, pady=5, sticky='news')

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


def process_file(filepath):
    p = Path(filepath)

    job = ffmpeg.input(filepath)

    # 30FPS
    job = job.filter('fps', fps=fps_var.get())

    info = ffmpeg.probe(filepath)

    pprint(info)

    stream = info['streams'][0]
    fmt = info['format']

    # Try to scale to 512px
    if stream['width'] >= stream['height']:
        job = job.filter('scale', 512, -1)
    else:
        job = job.filter('scale', -1, 512)

    if 'duration' in fmt:
        duration = float(fmt['duration'])

        # Try speed up video if it's over 3 seconds
        if duration > 3.0:
            job = job.filter('setpts', f"({limit_duration_var.get()}/{duration * 60})*PTS")

    out_path = str(p.with_suffix('.webm'))

    if os.path.exists(out_path):
        out_path = str(p.with_suffix('.telegram.webm'))

    job = (
        job
        .output(
            out_path,
            pix_fmt='yuva420p',
            vcodec='libvpx-vp9',
            an=None,  # Remove Audio
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
