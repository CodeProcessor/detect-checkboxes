# Simple Fast api application
import os
import aiofiles
from fastapi import FastAPI, UploadFile, File

from checkboxes import get_checkboxes_from_pdf

app = FastAPI()


@app.get("/")
def read_root():
    return {"Server": "UP!"}


@app.post("/checkboxes/")
async def find_checkboxes(
        file: UploadFile = File(..., alias="file", description="Attach the file to be processed"),
):
    _file_basename, _ext = os.path.splitext(file.filename)
    local_filename = "temp.pdf"
    async with aiofiles.open(local_filename, 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    return get_checkboxes_from_pdf(local_filename)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
