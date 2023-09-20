import uvicorn

from src.app import app
from settings import current_settings

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=current_settings.HOST,
        port=current_settings.PORT
    )
