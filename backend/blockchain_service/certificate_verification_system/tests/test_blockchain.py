import pytest
from ml_models.blockchain_integration.hash_generator import generate_hash_from_bytes

def test_hash_consistent():
    b = b'test-bytes'
    h1 = generate_hash_from_bytes(b)
    h2 = generate_hash_from_bytes(b)
    assert h1 == h2

def test_hash_change_with_content():
    h1 = generate_hash_from_bytes(b'a')
    h2 = generate_hash_from_bytes(b'b')
    assert h1 != h2
