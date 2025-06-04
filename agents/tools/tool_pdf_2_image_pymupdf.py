import fitz  # PyMuPDF
import os

def pdf_to_images_fitz(input_pdf: str, output_folder: str, dpi: int = 300):
    """
    Render PDF pages to PNG using PyMuPDF.

    Args:
        input_pdf: Path to source PDF.
        output_folder: Folder to save images into.
        dpi: Desired resolution.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    doc = fitz.open(input_pdf)
    zoom = dpi / 72  # 72 is the PDF's base resolution
    mat = fitz.Matrix(zoom, zoom)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=mat)
        print(f"pix: {pix}")
        out_path = f"{output_folder}/page_{page_num+1}.png"
        pix.save(out_path)
        print(f"Saved {out_path}")

    return out_path

if __name__ == "__main__":
    pdf_to_images_fitz("C:\\DDrive\\Programming\\Project\\ai-ml\\uv-project\\docs\\input.pdf", "C:\\DDrive\\Programming\\Project\\ai-ml\\uv-project\\docs\\images", dpi=300)