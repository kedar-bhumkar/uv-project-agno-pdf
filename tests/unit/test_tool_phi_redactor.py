import os
import pytest
from PIL import Image, ImageDraw
from agents.tools.tool_phi_redactor import redact_image

@pytest.fixture
def test_image(tmp_path):
    """Create a test image with some content."""
    # Create a white image with some colored rectangles
    img = Image.new('RGB', (200, 200), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw some colored rectangles that we'll redact
    draw.rectangle([50, 50, 100, 100], fill='red')    # Box 1
    draw.rectangle([120, 120, 180, 180], fill='blue') # Box 2
    
    # Save the test image
    input_path = tmp_path / "test_input.png"
    img.save(input_path)
    return str(input_path)

def test_redact_image(test_image, tmp_path):
    """Test that redact_image correctly blackens specified regions."""
    # Define boxes to redact
    boxes = [
        (50, 50, 100, 100),    # Red box
        (120, 120, 180, 180)   # Blue box
    ]
    
    # Create output path
    output_path = str(tmp_path / "test_output.png")
    
    # Perform redaction
    redact_image(test_image, output_path, boxes)
    
    # Verify the output file exists
    assert os.path.exists(output_path)
    
    # Load the redacted image
    redacted_img = Image.open(output_path)
    
    # Check that the redacted regions are black
    # Check first box (50,50,100,100)
    assert redacted_img.getpixel((75, 75)) == (0, 0, 0)  # Center of first box
    
    # Check second box (120,120,180,180)
    assert redacted_img.getpixel((150, 150)) == (0, 0, 0)  # Center of second box
    
    # Check that non-redacted regions remain white
    assert redacted_img.getpixel((10, 10)) == (255, 255, 255)  # Top-left corner
    assert redacted_img.getpixel((190, 190)) == (255, 255, 255)  # Bottom-right corner

def test_redact_image_empty_boxes(test_image, tmp_path):
    """Test that redact_image works with empty box list."""
    output_path = str(tmp_path / "test_output_empty.png")
    
    # Perform redaction with no boxes
    redact_image(test_image, output_path, [])
    
    # Verify the output file exists
    assert os.path.exists(output_path)
    
    # Load the redacted image
    redacted_img = Image.open(output_path)
    
    # Check that the image is unchanged
    original_img = Image.open(test_image)
    assert redacted_img.tobytes() == original_img.tobytes()

def test_redact_image_invalid_path():
    """Test that redact_image handles invalid input path."""
    with pytest.raises(FileNotFoundError):
        redact_image("nonexistent.png", "output.png", [(0, 0, 10, 10)])
