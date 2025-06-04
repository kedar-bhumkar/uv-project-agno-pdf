from typing import Dict, Any, List
from agno.agent import Agent
from agno.tools import tool
from agents.tools.tool_image_llm_parser import parse_clinical_document
from agents.tools.tool_phi_redactor import redact_image
from agno.models.openai import OpenAIChat
from agents.core.agent_prompts import prompt
from typing import Optional


  
def get_pdf_manager_agent(model_id: Optional[str] = "gpt-4.1", user_id: Optional[str] = "default", session_id: Optional[str] = "default", debug_mode: Optional[bool] = False):
    
    return Agent(
        name="PDF Manager Agent",
        context=["prompt", prompt],
        instructions=prompt,
        tools=[parse_clinical_document, redact_image],
        model=OpenAIChat(id="gpt-4o"),
        user_id=user_id,
        session_id=session_id,
        debug_mode=debug_mode,
        enable_agentic_memory= True,
        markdown=True
        
    )