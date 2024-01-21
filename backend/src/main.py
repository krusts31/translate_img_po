from .libpy.src.ft_get_file_extension import get_file_extension
from fastapi import FastAPI, File, UploadFile, HTTPException
from .middle_ware_upload_size import LimitUploadSize
from .translate_po import translate_po_file
from fastapi.responses import FileResponse
from starlette.responses import Response
from io import StringIO
import uvicorn
from uuid import uuid4
import os

app = FastAPI()
app.add_middleware(LimitUploadSize, max_upload_size=50_000_000)  # ~50MB

#check  name, type, contents, or size
#we are checking name, and size not sure about type and contents
@app.post("/upload-file")
async def upload_file(file: UploadFile = File()):
    """
        Cleanup: When an UploadFile object is garbage collected, its underlying temporary file is automatically deleted.
    """
    extension: str = get_file_extension(file.filename)

    if extension not in ["po", "png","jpeg", "jpg", "png"]:
        raise HTTPException(status_code=400, detail="Accepted types: po png jpeg jpg png")

    temp_file_path = "temp_" + str(uuid4()) + file.filename

    if extension == "po":
        try:
            with open(temp_file_path, 'wb') as out_file:
                contents = await file.read()
                out_file.write(contents)
            file_to_return: str = translate_po_file(temp_file_path)
            os.remove(temp_file_path)
            return FileResponse(file_to_return)
        except Exception as e:
            print("ERROR:", e)
            os.remove(temp_file_path)
            raise HTTPException(status_code=500, detail="Exception please contact 01gr0nd5")
    ontents = await file.read()

if __name__ == "__main__":
    uvicorn.run(app)
