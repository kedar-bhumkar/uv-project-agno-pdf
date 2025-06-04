from pydantic import BaseModel
from enum import Enum
from typing import Optional, Any, Dict

class Model(Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4_1 = "gpt-4.1"

class FileData(BaseModel):
    name: str
    type: str
    data: str

class AgentRunRequest(BaseModel):
    agent_id: str
    message: str
    stream: bool = False
    model: Model = Model.GPT_4O_MINI
    user_id: Optional[str] = "default"
    session_id: Optional[str] = "default"
    debug_mode: bool = False
    file_path: Optional[str] = None
    base64_file: Optional[FileData] = None  # Updated to use FileData model
 
    

class AgentResponse(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        arbitrary_types_allowed = True
    
