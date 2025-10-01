import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

def generate_qr(data: str, out_path: str):
    img = qrcode.make(data)
    img.save(out_path)
    return out_path

def decode_qr(image_path: str) -> str:
    img = Image.open(image_path)
    decoded = decode(img)
    if not decoded:
        return ''
    return decoded[0].data.decode('utf-8')

if __name__ == '__main__':
    # quick demo
    path = generate_qr('https://example.com/verify?hash=abc', '/tmp/demo_qr.png')
    print('Saved QR to', path)
