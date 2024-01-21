from fastapi.testclient import TestClient
from hypothesis import given, strategies, settings
from hypothesis.strategies import text
from .. import main
import tempfile
import os

test_count = int(os.environ["TEST_COUNT"])

client = TestClient(main.app)

@given(name=text(alphabet=strategies.characters(blacklist_characters="/\x00", whitelist_categories=('Lu', 'Ll'))),
       extension=text(alphabet='abcdefghijklmnopqrstuvwxyz'))
@settings(max_examples=test_count)
def test_upload_random_file(name: str, extension: str):
    with tempfile.NamedTemporaryFile(suffix="." + extension, prefix=name, mode='w+b') as temp_file:
        temp_file.write(b'Test content')
        temp_file.seek(0)

        files = {"file": (temp_file.name, temp_file, f'application/{extension}')}
        response = client.post("/upload-file", files=files)
        if extension not in ["po", "png","jpeg", "jpg", "png"]:
            assert response.status_code == 400
            assert response.json() == {"detail": "Accepted types: po png jpeg jpg png"}
        else:
            assert response.status_code == 200

@given(name=text(alphabet=strategies.characters(blacklist_characters="/\x00", whitelist_categories=('Lu', 'Ll'))))
@settings(max_examples=test_count)
def test_upload_accepted_file(name: str):
    for f in ["po", "png","jpeg", "jpg", "png"]:
        with tempfile.NamedTemporaryFile(suffix="." + f, prefix=name, mode='w+b') as temp_file:
            temp_file.write(b'Test content')
            temp_file.seek(0)
            files = {"file": (temp_file.name, temp_file, f'application/{f}')}
            response = client.post("/upload-file", files=files)
            assert response.status_code == 200

@given(name=text(alphabet=strategies.characters(blacklist_characters="/\x00", whitelist_categories=('Lu', 'Ll'))))
@settings(max_examples=test_count)
def test_upload_sneaky_file(name: str):
    for f in ["PO", "PNG","JPEG", "JPG", "PNG", "pO", "jPg"]:
        with tempfile.NamedTemporaryFile(suffix="." + f, prefix=name, mode='w+b') as temp_file:
            temp_file.write(b'Test content')
            temp_file.seek(0)
            files = {"file": (temp_file.name, temp_file, f'application/{f}')}
            response = client.post("/upload-file", files=files)
            assert response.status_code == 400
            assert response.json() == {"detail": "Accepted types: po png jpeg jpg png"}
