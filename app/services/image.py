import io
import uuid
from pathlib import Path
from fastapi import HTTPException, UploadFile
from PIL import Image

from app.core.exceptions import ApplicationException
from app.repositories.image import ImageRepository
from app.schemas.image import ImageResponse


class ImageService:
    def __init__(self, image_repo: ImageRepository):
        self.image_repo = image_repo
        self.UPLOAD_DIR = Path("uploads")
        self.ALLOWED_MIME_TYPES = ("image/png", "image/jpeg", "image/jpg")
        self.ALLOWED_IMAGE_FORMATS = ("PNG", "JPEG")
        self.MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024 # 2MB

    
    async def upload(self, file: UploadFile, user_id: int) -> ImageResponse:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        if not file.content_type or not file.content_type.startswith("image/") or file.content_type not in self.ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=415, detail="Unsupported file type. Only image files are allowed.")
        filename = f"{str(uuid.uuid4())}_{file.filename}"
        file_path = self.UPLOAD_DIR / filename
        self.UPLOAD_DIR.mkdir(exist_ok=True)
        try:
            file_content_bytes = await file.read()
            file_size = len(file_content_bytes)
            image = Image.open(io.BytesIO(file_content_bytes))
            image.verify()
            if image.format not in self.ALLOWED_IMAGE_FORMATS:
                raise HTTPException(
                    status_code=415,
                    detail="Only JPEG and PNG images are allowed."
                )
            if file_size > self.MAX_FILE_SIZE_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail=f"File size exceeds the maximum allowed limit of {self.MAX_FILE_SIZE_BYTES / (1024 * 1024):.0f}MB."
                )
            image_metadata_dict = {
                "format": image.format,
                "mode": image.mode,
                "width": image.size[0],
                "height": image.size[1],
            }
            with open(file_path, 'wb') as buffer:
                buffer.write(file_content_bytes)
            return ImageResponse(
                id=user_id,
                url=f"http://localhost:8000/uploads/{filename}",
                image_metadata=image_metadata_dict
            )
        except Image.UnidentifiedImageError:
            raise HTTPException(
                status_code=400,
                detail="Could not identify image file. It might be corrupted or not a valid image."
            )
        except Exception:
            raise ApplicationException
