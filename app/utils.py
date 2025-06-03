from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from .settings import settings
import os
from pathlib import Path
from uuid_extensions import uuid7


async def save_file(file: UploadFile, parent_folder: str) -> str:
        
        if not file:
           default_file = 'defaults/contact-icon-illustration-isolated_23-2151903337.jpg'
           default_folder = os.path.join('static', default_file)
           return default_folder
        contents = await file.read()

        
        if len(contents) > settings.MAX_FILE_SIZE * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="File too large. Maximum size is 2MB."
            )
        
        file_path = os.path.join(settings.STATIC_FILES, parent_folder)
        os.makedirs(file_path, exist_ok=True)
        file_name =  f'{uuid7()}_{file.filename}'
        main_file_path = os.path.join(file_path,file_name)
        with open(main_file_path, "wb") as f:
            f.write(contents)

        return f"/static/{parent_folder}/{file_name}"