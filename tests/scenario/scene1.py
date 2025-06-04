import os
import tempfile

import pytest
from PIL import Image, ImageDraw
from scenario import Scenario, TestingAgent

from agents.core.agent_def import get_pdf_manager_agent

Scenario.configure(testing_agent=TestingAgent(model="openai/gpt-4o-mini"))


@pytest.fixture
def test_image():
    """Create a test image with some content."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        # Create a white image with some colored rectangles
        img = Image.new("RGB", (200, 200), "white")
        draw = ImageDraw.Draw(img)

        # Draw some colored rectangles that we'll redact
        draw.rectangle([50, 50, 100, 100], fill="red")  # Box 1
        draw.rectangle([120, 120, 180, 180], fill="blue")  # Box 2

        # Save the test image
        img.save(tmp.name)
        return tmp.name


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_pdf_manager_agent_scenario():
    """Test scenario for PDF Manager Agent's document handling capabilities."""

    # Create the agent
    agent = get_pdf_manager_agent(model_id="gpt-4", user_id="test_user", session_id="test_session", debug_mode=True)

    # Create a callable function that uses the agent
    async def agent_function(message, context):
        response = agent.run(message)
        # Convert the response to a format expected by Scenario
        # return {
        #     "content": str(response.content),
        #     "role": "assistant",
        #     "type": "text"
        # }
        return {"messages": [{"role": "assistant", "content": response.content}]}

    # Define the scenario
    scenario = Scenario(
        "Parse the given pdf and return structured output",
        agent=agent_function,
        success_criteria=[
            "Document parsing returns a valid dictionary with extracted information",
            "Redaction process successfully creates a new redacted image file",
        ],
        failure_criteria=[
            "Document parsing fails to return a valid dictionary",
            "Redaction process fails to create a new redacted image file",
        ],
        max_turns=5,
    )
    
    # Run the scenario and get results
    result = await scenario.run()

    # Assert for pytest to know whether the test passed
    assert result.success
