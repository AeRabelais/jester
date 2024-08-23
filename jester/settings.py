from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )

    openai_key: str = Field(validation_alias="OPENAI_API_KEY")
    mandatory_skills: list[str] = [

    ]
    optional_skills: list[str] = [ ] 
    
    popular_languages = [
        "python",
        "javascript",
        "java",
        "c++",
        "c#",
        "ruby",
        "php",
        "typescript",
        "sql",
        "kotlin",
        "r"
    ]

settings = Settings()