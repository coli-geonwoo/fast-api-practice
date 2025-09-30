from fastapi import APIRouter, status, UploadFile, File, Depends
from fastapi.responses import JSONResponse, FileResponse

from services.ml_service import MlService, get_ml_service

router = APIRouter(
    prefix="/ml",
    tags=["ml"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}

)

@router.post(
    "/predict/{user_id}",
    summary = "이미지 업로드 . 예측 결과 반환",
    # response_model = JSONResponse
)
async def predict(
        user_id : int,
        image : UploadFile = File(...),
        service: MlService = Depends(get_ml_service)
):
    result = await service.predict(image, user_id)
    return JSONResponse(result)

@router.get(
    "/myImage/{filename}/{user_id}",
    summary = "이미지 가져오기",
    # response_model = FileResponse
)
def get_my_image(
        filename : str,
        user_id : int,
        service: MlService = Depends(get_ml_service)
):
    result = service.get_my_image(filename, user_id)
    return FileResponse(result, media_type="image/png") # png 타입만 반환 'image/*' == 이미지 파일이면 모두 반환가능
