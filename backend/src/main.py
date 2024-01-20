from .libpy.src.ft_get_file_extension import get_file_extension
from fastapi import FastAPI, File, UploadFile, HTTPException
from .middle_ware_upload_size import LimitUploadSize
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

@app.post("/upload-file")
async def upload_file(file: UploadFile = File()):
    """
        Cleanup: When an UploadFile object is garbage collected, its underlying temporary file is automatically deleted.
    """
    if get_file_extension(file.filename) not in ["po", "png","jpeg", "jpg", "png"]:
        raise HTTPException(status_code=400, detail="Accepted types: po png jpeg jpg png")
    ontents = await file.read()
    return {"filename": file.filename}

if __name__ == "__main__":
    uvicorn.run(app)
