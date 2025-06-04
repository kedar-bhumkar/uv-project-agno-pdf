from fastapi import APIRouter, status, HTTPException
from fastapi.responses import StreamingResponse
from agents.core.selector import get_available_agents, get_agent_by_type
from agents.core.selector import AgentType
from typing import List
from agno.agent import Agent
from apps.routes.model import AgentRunRequest, AgentResponse
import base64
import os


agents_router = APIRouter(prefix="/agents", tags=["Agents"])


async def agent_response_streamer(agent: Agent, message: str):
    
    response = await agent.arun(message, stream=True)
    
    async for chunk in response:
        yield chunk.content



@agents_router.get("", response_model=List[str])
async def list_agents():
    """
    List all available agents
    """
    return get_available_agents()




@agents_router.post("/{agent_id}/run", status_code=status.HTTP_200_OK, response_model=AgentResponse)
async def run_agent(run_request: AgentRunRequest):
    """
    Run an agent by type
    agent_id: str
    run_request: AgentRunRequest

    """
    
    
    try:
        agent = get_agent_by_type(
                                  agent_type=AgentType(run_request.agent_id),
                                  model_id=run_request.model,
                                  user_id=run_request.user_id,
                                  session_id=run_request.session_id,
                                  debug_mode=run_request.debug_mode
                                  )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Agent {run_request.agent_id} not found")

    if run_request.stream:
        print("Streaming response")
        return StreamingResponse(agent_response_streamer(agent, run_request.message), media_type="text/event-stream")
    else:
        print("Non-streaming response")
        # Create a dictionary with message and base64_file if present
        agent_input = {"message": run_request.message}
        if run_request.base64_file:
            # Write base64 data to file
            output_dir = r"C:\DDrive\Programming\Project\ai-ml\uv-project\docs"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "page_1.png")
            
            try:
                # Decode base64 data and write to file
                image_data = base64.b64decode(run_request.base64_file.data)
                print(f"Image data: {image_data}")
                with open(output_path, "wb") as f:
                    f.write(image_data)
                print(f"Image saved to: {output_path}")
                
                # Add the file path to the agent input
                agent_input["base64_file"] = run_request.base64_file.data
                agent_input["file_path"] = output_path
                agent_input["file_name"] = run_request.base64_file.name
                agent_input["file_type"] = run_request.base64_file.type
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to save image: {str(e)}"
                )
            
        response = await agent.arun(run_request.message, stream=False)
        print(f"Response: {response}")
        return AgentResponse(
            content=response.content,
            metadata=response.metadata if hasattr(response, 'metadata') else None
        )
       
    
    
    
    

