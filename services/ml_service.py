from datetime import datetime

from fastapi import UploadFile
from typing import Any, Union
from pathlib import Path

from exception.exceptions import UnauthorizedError, ImageNotFoundError


class MlService:
    # 순서대로 들어오지 않고 key, value 형태로 객체를 생성하도록 강제
    def __init__(self, *, storage_dir: Union[str | Path] = "S3"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)  # 부모 디렉토리가 없어도 생성하겠니?, exists_ok: 이미 존재해도 생성강제

    async def predict(self, image: UploadFile, user_id: int) -> dict[str, Any]:
        # 파일명 생성 : {user_id}-{upload_time}.{ext}
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        # includes leading dot , e.g "png"
        ext = Path(image.filename or "").suffix
        filename = f"{user_id}-{ts}.{ext}" if ext else f"{user_id}-{ts}"
        save_path = self.storage_dir / filename

        content = await image.read()
        save_path.write_bytes(content)

        return {
            "filename": filename,
        }

    def get_my_image(
            self,
            filename: str,
            user_id: int
    ):
        image_name = Path(filename).name

        #소유권 검증
        if(not image_name.startswith(f"{user_id}-")) :
            raise UnauthorizedError()

        #path에서 직접 찾기
        image_path = self.storage_dir / image_name

        if not image_path.exists() or not image_path.is_file():
            raise ImageNotFoundError()

        return image_path




ml_service = MlService()


def get_ml_service():
    return ml_service
