from fastapi import FastAPI, HTTPException
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from prisma import Prisma

from app.add_files import is_valid_audio_file

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/music", StaticFiles(directory="tmp/music"), name="static")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/songs")
async def get_song():
    async with Prisma() as prisma:
        songs = await prisma.song.find_many()
        return songs


@app.post("/v1/songs")
async def create_song(song: dict):
    async with Prisma() as prisma:
        created_song = await prisma.song.create(data=song)
        return created_song


@app.get("/v1/songs/{id}")
async def get_song_by_id(id: int):
    async with Prisma() as prisma:
        song = await prisma.song.find_unique(where={'id': id})
        return song


@app.get("/files/{file_path:path}")
async def main(file_path):
    print(file_path)
    return FileResponse(file_path)


@app.post("/uploadfile")
def create_upload_file(file: UploadFile):
    if not is_valid_audio_file(file):
        raise HTTPException(status_code=400, detail="Invalid audio file")

    with open(f"tmp/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    return {"filename": file.filename}
