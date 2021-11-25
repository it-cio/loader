import os
import shutil
import uvicorn
from typing import List
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()


@app.get("/authorization")  # basic authorization
def users(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}


@app.post("/upload")  # image loader
async def image(files: List[UploadFile] = File(...)):
    save_list = []
    for img in files:
        if 'image' in img.content_type and len(img.file.read()) < 200000:  # check for content is image and image size not above 200kb
            if not os.path.isdir('img'):  # check if in root directory exist 'img' folder
                os.mkdir('img')  # if 'img' folder not exist create him
            with open(f"img/{img.filename}", "wb") as buffer:  # save content in buffer
                shutil.copyfileobj(img.file, buffer)  # save file in 'img' folder
            save_list.append(img.filename)

    return {"saved_files": save_list}


if __name__ == '__main__':  # start local uvicorn server
    uvicorn.run('main:app', reload=True)