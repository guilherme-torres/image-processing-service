import io
from urllib.parse import urlparse
from typing import Any, Union
import uuid
from pathlib import Path
from fastapi import HTTPException, UploadFile
from PIL import Image, ImageFilter

from app.core.exceptions import ApplicationException
from app.repositories.image import ImageRepository
from app.schemas.image import ImageCreate, ImageResponse
from app.schemas.transformations import Crop, Filters, Resize, TransformationsCreate


class ImageService:
    def __init__(self, image_repo: ImageRepository):
        self.image_repo = image_repo
        self.UPLOAD_DIR = Path("uploads")
        self.ALLOWED_MIME_TYPES = ("image/png", "image/jpeg", "image/jpg")
        self.ALLOWED_IMAGE_FORMATS = ("PNG", "JPEG")
        self.MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024 # 2MB

    
    def save_image(self, image_content: bytes, local_path: Union[str, Path, None] = None) -> None:
        if local_path:
            # salvar no filesystem
            try:
                with open(local_path, 'wb') as buffer:
                    buffer.write(image_content)
            except IOError:
                raise HTTPException(status_code=500, detail="Failed to save image to local storage.")
        
        # salvar em um storage na nuvem
        return None

    
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
            image.save(file_path)
            image.close()

            # self.save_image(file_content_bytes, local_path=file_path)

            image_url = f"http://localhost:8000/uploads/{filename}"
            image_create_dict = ImageCreate(
                url=image_url,
                image_metadata=image_metadata_dict,
            ).model_dump()
            image_create_dict["user_id"] = user_id
            self.image_repo.create(image_create_dict)

            return ImageResponse(
                id=user_id,
                url=image_url,
                image_metadata=image_metadata_dict
            )
        except Image.UnidentifiedImageError:
            raise HTTPException(
                status_code=400,
                detail="Could not identify image file. It might be corrupted or not a valid image."
            )
        except Exception:
            raise ApplicationException
        
    
    def get_image_by_id(self, id: int, user_id: int) -> ImageResponse:
        image = self.image_repo.get(id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found.")
        return ImageResponse(
            id=image.id,
            url=image.url,
            image_metadata=image.image_metadata,
        )
    

    def list_images(self, user_id: int, skip: int = 0, limit: int = 100) -> list[ImageResponse]:
        images = self.image_repo.get_all(limit=limit, skip=skip, filter_by={"user_id": user_id})
        return [
            ImageResponse(
                id=image.id,
                url=image.url,
                image_metadata=image.image_metadata
            ) for image in images
        ]
    

    def delete_image(self, id: int, user_id: int) -> bool:
        image = self.image_repo.get(id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found.")
        if image.user_id != user_id:
            raise HTTPException(status_code=403, detail="Operation not permitted.")
        return self.image_repo.delete(id)
    

    def apply_transformation(self, image: Image.Image, transform_name: str, value: Any):
        def resize(options: dict) -> Image.Image:
            return image.resize(size=(options["width"], options["height"]))
        def crop(options: dict) -> Image.Image:
            return image.crop(box=(
                options["x"],
                options["y"],
                options["x"] + options["width"],
                options["y"] + options["height"]
            ))
        def rotate(angle: float) -> Image.Image:
            return image.rotate(angle)
        def change_format(format_name: str) -> Image.Image:
            return image
        def apply_filters(options: dict) -> Image.Image:
            for filter_option in options.keys():
                match filter_option:
                    case "grayscale":
                        return image.convert(mode="L")
                    case "sepia":
                        return image.convert(mode="RGB", matrix=(
                            0.393, 0.769, 0.189, 0,
                            0.349, 0.686, 0.168, 0,
                            0.272, 0.534, 0.131, 0
                        ))
                    case _:
                        raise Exception("Invalid filter.")
            return image
        transformations = {
            "resize": resize,
            "crop": crop,
            "rotate": rotate,
            "format": change_format,
            "filters": apply_filters,
        }
        return transformations[transform_name](value)
    

    def transform(self, id: int, user_id: int, transformations_dict: dict) -> ImageResponse:
        print(transformations_dict)
        image = self.image_repo.get(id)
        if not image:
            raise Exception("Image not found.")
        if image.user_id != user_id:
            raise Exception("Operation not permitted.")
        parsed_url = urlparse(image.url)
        filename = parsed_url.path.split("/")[-1]
        print("filename:", filename)
        file_path = self.UPLOAD_DIR / filename
        with Image.open(file_path) as image_file:
            if transformations_dict["transformations"]:
                image_copy = image_file.copy()
                for transformation_name, value in transformations_dict["transformations"].items():
                    image_copy = self.apply_transformation(
                        image_copy,
                        transform_name=transformation_name,
                        value=value
                    )
                filename = f"{str(uuid.uuid4())}_{''.join(filename.split('_')[1:])}"
                print(filename)
                image_copy.save(self.UPLOAD_DIR / filename)
                image_metadata_dict = {
                    "format": image_copy.format,
                    "mode": image_copy.mode,
                    "width": image_copy.size[0],
                    "height": image_copy.size[1],
                }
                image_create_dict = ImageCreate(
                    url=f"http://localhost:8000/uploads/{filename}",
                    image_metadata=image_metadata_dict,
                ).model_dump()
                image_create_dict["user_id"] = user_id
                created_image = self.image_repo.create(image_create_dict)
                return ImageResponse(
                    id=created_image.id,
                    url=created_image.url,
                    image_metadata=created_image.image_metadata,
                )
        return ImageResponse(
            id=image.id,
            url=image.url,
            image_metadata=image.image_metadata,
        )
