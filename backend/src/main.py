from .middle_ware_upload_size import LimitUploadSize
from fastapi import FastAPI, File, UploadFile, HTTPException
from starlette.responses import Response
import uvicorn

app = FastAPI()
#
#replace this with nginx proxy protection
#not bad for now
app.add_middleware(LimitUploadSize, max_upload_size=50_000_000)  # ~50MB

@app.get("/")
async def read_root():
    return {'msg': 'Hello World'}

def check_file_type(file_name: str, accepted_file_types: [str]) -> bool:
    try:
        file_extension: str = file_name.rsplit('.', 1)[1]
        if file_extension not in accepted_file_types:
            return False
    except Exception as e:
        return False

@app.post("/upload-file")
async def upload_file(file: UploadFile = File()):
    """
        Cleanup: When an UploadFile object is garbage collected, its underlying temporary file is automatically deleted.
    """
    print(file.filename, flush=True)
    if not check_file_type(file.filename, ["po", "png","jpeg", "jpg", "png"]):
        raise HTTPException(status_code=400, detail="Accepted types: po png jpeg jpg png")
    ontents = await file.read()
    return {"filename": file.filename}

if __name__ == "__main__":
    uvicorn.run(app)
