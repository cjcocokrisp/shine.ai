from pathlib import Path
from PIL import Image
import os

path = input('List the directory to convert to all pngs: ')
path = Path(path)

for file in path.iterdir():
    file = str(file)
    if file.find('.png') == -1 and file.find('.PNG') == -1:
        img = Image.open(file)
        img.convert('RGB')
        img.save(file.replace(file[file.find('.') + 1:], 'png'), 'png')
        img.close()
        os.remove(file)