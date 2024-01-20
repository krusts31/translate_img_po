from hypothesis import given, strategies as st

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

#upload a file .po extension
#output a .po or .mo file

#upload a file .img or similar extension
#output a .txt file
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

@given(st.integers())
def test_home(s):
    res = client.get(f"/api/{s}")

    assert res.status_code == 200
    assert res.json() == {"message": s * s}


def test_read_post():
    response = client.post("/upload-file")
    response = client.post(
        "/upload-file", files={"file": ("filename", open("po/woocommerce-lv.po", "rb"), ".po")}
    )
    assert response.status_code == 200
    #assert response.json() == {"msg": "Hello World"}
