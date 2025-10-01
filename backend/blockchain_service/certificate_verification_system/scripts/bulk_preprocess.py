import os, glob
from PIL import Image, ImageFilter
SRC = 'data/raw'
DST = 'data/processed'

os.makedirs(DST, exist_ok=True)

def preprocess_image(path, out_path):
    img = Image.open(path).convert('L')
    img = img.resize((1200, int(1200 * img.height / img.width))) if img.width > 1200 else img
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img.save(out_path)

if __name__ == '__main__':
    files = glob.glob(os.path.join(SRC, '*.*'))
    for f in files:
        name = os.path.basename(f)
        out = os.path.join(DST, name)
        try:
            preprocess_image(f, out)
            print('Processed', name)
        except Exception as e:
            print('Failed', name, e)
