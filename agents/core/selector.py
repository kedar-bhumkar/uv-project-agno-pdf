from enum import Enum
from agents.core.agent_def import get_pdf_manager_agent
from typing import List
from typing import Optional

class AgentType(Enum):
    PDF_MANAGER = "pdf_manager_agent"


def get_available_agents()->List[str]:
  return [agent.value for agent in AgentType]
 

def get_agent_by_type(agent_type: AgentType, model_id: Optional[str] = "gpt-4o-mini", user_id: Optional[str] = "default", session_id: Optional[str] = "default", debug_mode: Optional[bool] = False):
    if agent_type == AgentType.PDF_MANAGER:
        return get_pdf_manager_agent(model_id=model_id, user_id=user_id, session_id=session_id, debug_mode=debug_mode)
    else:
        raise ValueError(f"Agent type {agent_type} not found")
