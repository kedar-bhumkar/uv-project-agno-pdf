from PIL import Image, ImageDraw

def redact_image(input_path: str, output_path: str, boxes: list[tuple[int,int,int,int]]) -> None:
    """
    Redacts (black-out) specified rectangular regions in an image.

    Args:
        input_path:  Path to the source image.
        output_path: Path where the redacted image will be saved.
        boxes:       A list of 4-tuples (left, top, right, bottom) defining regions to redact.
    """ 
    # Load image
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)

    # Draw black rectangles over each box
    for (left, top, right, bottom) in boxes:
        draw.rectangle([left, top, right, bottom], fill="black")

    # Save result
    img.save(output_path)
    print(f"Redacted image saved to {output_path}")

    return output_path

# if __name__ == "__main__":
#     # Example usage:
#     INPUT_FILE  = "docs/output/page_1.png"
#     OUTPUT_FILE = "docs/output/redacted.png"

#     # Replace these with the actual pixel coords you need to redact
#     PHI_BOXES = [
#         (656,  352, 927, 394),   # e.g. Member Name
#         (1383,  348, 1612, 391),   # e.g. Date of Birth
#         (1883,  343, 2206,389),   # e.g. ID
#     ]

#     redact_image(INPUT_FILE, OUTPUT_FILE, PHI_BOXES)
