from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# 1. 클래스 외부에서 환경 파일 목록을 결정하는 함수 정의
def get_env_files():
    env = os.getenv("APP_ENV", "local")
    # 기본 .env는 항상 읽고, 환경이 dev라면 .env.dev를 추가로 읽어 덮어씌움
    if env == "dev":
        return (".env", ".env.dev")
    return (".env",)

class Settings(BaseSettings):
    OPENAI_API_KEY: str    
    BASE_URL: str
    SUMMARY_PATH: str
    
    model_config = SettingsConfigDict(env_file=get_env_files())

settings = Settings()