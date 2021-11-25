import uvicorn
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.post("/upload")
async def image(files: List[UploadFile] = File(...)):
    save_list = []
    for img in files:
        with open(f"img/{img.filename}", "wb") as file:
            shutil.copyfileobj(img.file, file)
        save_list.append(img.filename)

    return {"saved_files": save_list}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)