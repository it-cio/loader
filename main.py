import os
import uvicorn
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.post("/upload")
async def image(files: List[UploadFile] = File(...)):
    save_list = []
    for img in files:
        if 'image' in img.content_type and len(img.file.read()) < 200000:
            if not os.path.isdir('img'):
                os.mkdir('img')
            with open(f"img/{img.filename}", "wb") as buffer:
                shutil.copyfileobj(img.file, buffer)
            save_list.append(img.filename)

    return {"saved_files": save_list}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)