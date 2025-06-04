from typing import Dict, Any
from agno.workflow import Workflow
from agents.tools.tool_image_llm_parser import *
from agents.tools.tool_phi_redactor import *
from agents.tools.tool_pdf_2_image_pymupdf import *
import os
import json

class PDFProcessingWorkflow(Workflow):
    def __init__(self):
        super().__init__(
            name="PDF Processing Workflow",
            description="Process PDF documents through conversion, redaction, and parsing"
        )
    
    def convert_pdf_to_images(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Convert PDF to images using pdf_to_images_fitz"""
        input_pdf = context["input_pdf"]
        output_dir = context["output_dir"]
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        images_dir = os.path.join(output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        pdf_to_images_fitz(input_pdf, images_dir, dpi=300)
        return {"images_dir": images_dir, "output_dir": output_dir}
    
    def redact_phi(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Redact PHI information from images"""
        images_dir = context["images_dir"]
        output_dir = context["output_dir"]
        input_image = os.path.join(images_dir, "page_1.png")
        redacted_image = os.path.join(images_dir, "redacted.png")
        
        # Example PHI boxes - these should be configured based on document layout
        phi_boxes = [
            (656, 352, 927, 394),    # Example: Member Name
            (1383, 348, 1612, 391),  # Example: Date of Birth
            (1883, 343, 2206, 389),  # Example: ID
        ]
        
        redact_image(input_image, redacted_image, phi_boxes)
        return {"redacted_image": redacted_image, "output_dir": output_dir}
    
    def parse_document(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the document using LLM"""
        redacted_image = context["redacted_image"]
        output_dir = context["output_dir"]
        
        result = parse_clinical_document(redacted_image)
        
        # Save the parsed results
        output_json = os.path.join(output_dir, "parsed_result.json")
        with open(output_json, 'w') as f:
            json.dump(result, f, indent=2)
            
        return {"parsed_result": result, "output_json": output_json}
    
    def run(self, input_pdf: str, output_dir: str) -> Dict[str, Any]:
        """Execute the complete workflow"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        context = {
            "input_pdf": input_pdf,
            "output_dir": output_dir
        }
        
        # Execute each method in sequence
        context = self.convert_pdf_to_images(context)
        context = self.redact_phi(context)
        context = self.parse_document(context)
        
        return context

# # Example usage
# if __name__ == "__main__":
#     workflow = PDFProcessingWorkflow()
#     result = workflow.run(
#         input_pdf="docs/input.pdf",
#         output_dir="docs/output"
#     )
