import os
import shutil
import uvicorn
from typing import List
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()


@app.get("/authorization")
def users(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}


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