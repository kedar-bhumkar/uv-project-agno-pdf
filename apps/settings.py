from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

class ApiSettings(BaseSettings):

    title: str = Field(default="Agno pdf agent")
    description: str = Field(default="Agno pdf agent")
    version: str = Field(default="1.0.0")

    runtime_env: str = Field(default="dev")

    docs_enabled: bool = Field(default=True)

    cors_origins_list: Optional[List[str]] = Field(default=["*"], validate_default=True)

    @field_validator("cors_origins_list", mode="before")
    def set_cors_origins(cls, cors_origin_list, info: FieldValidationInfo):
        """
        Validates and sets CORS origins for the API.
        
        Args:
            cors_origin_list: List of CORS origins from environment variable
            info: Field validation info
            
        Returns:
            List of valid CORS origins including default development origins
        """
        # Initialize with provided origins or empty list
        valid_cors = cors_origin_list or []
        
        # Add default development origins
        default_origins = [
            "https://*.ngrok.io",
            "https://app.agno.com", 
            "https://localhost",
            "http://localhost:3000"
        ]
        valid_cors.extend(default_origins)
        
        return valid_cors
    
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

api_settings = ApiSettings()