import os
from openai import OpenAI
import json
from typing import Dict, Any
import base64

def parse_clinical_document(image_path: str) -> Dict[str, Any]:
    """
    Parse a clinical document image using OpenAI's GPT-4 Vision model and return structured JSON.
    
    Args:
        image_path (str): Path to the clinical document image
        
    Returns:
        Dict[str, Any]: Structured JSON containing parsed information from the clinical document
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print(f"image_path: {image_path}")
    
    # Read the image file and encode it in base64
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare the prompt for the model
    prompt = """Please analyze this clinical document image and extract all relevant information. 
    Return the information in a well-structured JSON format. Use the same labels for json keys as defined in the image.     
    Format the response as a valid JSON object with appropriate nesting and data types.
    IMPORTANT: Your response must be a valid JSON object only, with no additional text before or after.
    Do not include ```json at the beginning or end of your response."""
    
    try:
        # Call the GPT-4 Vision model
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_data}"
                            }
                        }
                    ]
                }
            ]
        )
        
        # Extract the response text
        response_text = response.choices[0].message.content.strip()
        
        # Debug: Print the raw response
        print("Raw API Response:", response_text)
        
        try:
            # Try to parse the JSON response
            parsed_json = json.loads(response_text)
            return parsed_json
        except json.JSONDecodeError as json_err:
            # If JSON parsing fails, try to clean the response
            # Remove any potential markdown code block markers
            cleaned_text = response_text.replace('```json', '').replace('```', '').strip()
            try:
                return json.loads(cleaned_text)
            except json.JSONDecodeError:
                raise Exception(f"Failed to parse JSON response: {json_err}\nResponse text: {response_text}")
        
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

# if __name__ == "__main__":
#     # Example usage
#     image_path = "docs/images/redacted.png"
#     try:
#         result = parse_clinical_document(image_path)
#         print("\nParsed JSON Result:")
#         print(json.dumps(result, indent=2))
#     except Exception as e:
#         print(f"Error: {str(e)}")
