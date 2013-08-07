import os
import subprocess
import random

if os.name == 'nt':
    ffmpeg_path =  "ffmpeg.exe %s" # WARNING Poner ruta a ffmpeg para windows
else:
    ffmpeg_path = 'ffmpeg' # Comando

DEVNULL = open(os.devnull, 'wb')

def video_thumb(from_, to, size):
    # def parse_string(text):
    #     """Parsear string para consola Bash.
    #     """
    #     for f, t in (("'", "'\"'\"'"),):
    #         text = text.replace(f, t)
    #     return text
    # from_ = parse_string(from_)
    # to = parse_string(to)
    args = [
        ffmpeg_path, '-y', '-ss', str(300 + random.randint(0, 300)),
        '-i', from_, '-f', 'mjpeg', '-vframes', '1', '-s',
        '%ix%i' % size, '-an', to
    ]
    try:
        return subprocess.call(args, stdout=DEVNULL, stderr=DEVNULL)
    except:
        return 1