from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.templating import Jinja2Templates

# =============> templating
templates = Jinja2Templates(directory="templates")


# =============> settings (dotenv)
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_title: str = "FastAPI"
    root_path: str = ""


settings = Settings(_env_file=".env")

