import io

from fastapi import FastAPI, UploadFile, status, Response, File
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from PIL import Image

from src.model import SegformerSegmenter
from settings import current_settings
from utils import img2bytes

app = FastAPI()
segmenter = SegformerSegmenter(
    model_path=current_settings.MODEL_PATH
)

@app.get('/')
def redir_to_docs() -> RedirectResponse:
    """Редирект на страницу с /docs.

    @return: RedirectResponse
    """
    return RedirectResponse('/docs')

@app.post('/api/segmentation_img')
def predict(file: UploadFile=File(...)):
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    try:
        img = Image.open(file.file)
        seg_img = segmenter.get_segments_img(img)

        return Response(content=img2bytes(seg_img), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))