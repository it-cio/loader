import os
import shutil
import uvicorn
import secrets
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "Tester")  # simple username and password
    correct_password = secrets.compare_digest(credentials.password, "qwerty123")  # to pass verification
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/upload")  # image loader
async def image(files: List[UploadFile] = File(...), username: str = Depends(get_current_username)):
    save_list = []
    for img in files:
        if 'image' in img.content_type and len(img.file.read()) < 200000:  # check for content is image and image size not above 200kb
            if not os.path.isdir('img'):  # check if in root directory exist 'img' folder
                os.mkdir('img')  # if 'img' folder not exist create him
            with open(f"img/{img.filename}", "wb") as buffer:  # save content in buffer
                shutil.copyfileobj(img.file, buffer)  # save file in 'img' folder
            save_list.append(img.filename)
    return {f"{username} saved_files": save_list}


if __name__ == '__main__':  # start local uvicorn server
    uvicorn.run('main:app', reload=True)