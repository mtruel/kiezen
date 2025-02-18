import magic
from fastapi import UploadFile


def is_valid_audio_file(file: UploadFile):
    mime_type = magic.from_buffer(file.file.read(2048), mime=True)
    print(mime_type)
    if not mime_type.startswith("audio/"):
        return False
    if file.filename == "":
        return False
    return True
