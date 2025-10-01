import hashlib
import json
import os
from PIL import Image
import io

def normalize_text(text: str) -> str:
    # simple canonicalization: strip, lowercase, collapse whitespace
    return ' '.join(text.strip().lower().split())

def file_bytes(path: str) -> bytes:
    # read binary file content
    with open(path, 'rb') as f:
        return f.read()

def generate_hash_from_bytes(data_bytes: bytes) -> str:
    h = hashlib.sha256()
    h.update(data_bytes)
    return h.hexdigest()

def generate_hash_from_file(path: str, include_image_normalization: bool = True) -> str:
    """Generate SHA256 hash from a certificate file.
    If include_image_normalization=True, we convert to a canonical PNG bytes (grayscale, resized)
    to improve robustness to minor variations.
    """
    if include_image_normalization:
        try:
            img = Image.open(path).convert('L')  # grayscale
            img = img.resize((1200, int(1200 * img.height / img.width))) if img.width > 1200 else img
            bio = io.BytesIO()
            img.save(bio, format='PNG', optimize=True)
            data = bio.getvalue()
        except Exception:
            data = file_bytes(path)
    else:
        data = file_bytes(path)
    return generate_hash_from_bytes(data)

if __name__ == '__main__':
    # simple demo
    import sys
    if len(sys.argv) > 1:
        print(generate_hash_from_file(sys.argv[1]))
    else:
        print('Usage: python hash_generator.py <path-to-certificate>')
