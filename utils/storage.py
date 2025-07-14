import os

from fastapi import UploadFile

from aiofile import async_open

from uuid import uuid4

from core.config import settings


class Storage:
    def verify_ext_file(file: UploadFile) -> bool:
        ext_file: str = file.filename.split('.')[-1]

        if ext_file != "png" and ext_file != "jpeg" and ext_file != "jpg":
            return False

        return True

    def generate_hash_filename(file: UploadFile) -> str:
        ext_file: str = file.filename.split('.')[-1]
        filename: str = f"{str(uuid4())}.{ext_file}"

        return filename

    async def upload_file(filename: str, path: str, file: UploadFile) -> None:
        if not os.path.exists(f"./{settings.UPLOAD_DIR}/{path}"):
            os.makedirs(f"./{settings.UPLOAD_DIR}/{path}")

        async with async_open(f"./{settings.UPLOAD_DIR}/{path}/{filename}", "wb") as afile:
            await afile.write(file.file.read())

    def delete_file(file_path: str, path: str) -> None:
        if os.path.isfile(f"./{settings.UPLOAD_DIR}/{path}/{file_path}"):
            os.remove(f"./{settings.UPLOAD_DIR}/{path}/{file_path}")
            