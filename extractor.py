import fitz  # PyMuPDF
from PIL import Image
import io

def extract_from_pdf(file_stream, prefix="doc"):
    """
    Extracts text and embedded images from a PDF file stream.
    Returns:
        text (str): The concatenated text of the entire document.
        images (list): A list of dicts containing image metadata and the PIL Image object.
            [{"id": "doc_image_1", "image": PIL.Image, "page": 1, ...}]
    """
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    
    full_text = ""
    extracted_images = []
    
    image_counter = 1
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract text from this page
        page_text = page.get_text()
        full_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
        
        # Extract images from this page
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            try:
                # Convert to PIL Image
                image = Image.open(io.BytesIO(image_bytes))
                
                # Filter out very small images (like logos or icons) that might not be relevant
                if image.width > 100 and image.height > 100:
                    image_id = f"{prefix}_img_{image_counter}"
                    extracted_images.append({
                        "id": image_id,
                        "image": image,
                        "page": page_num + 1,
                        "format": image_ext
                    })
                    image_counter += 1
            except Exception as e:
                print(f"Failed to process image on page {page_num + 1}: {e}")
                
    doc.close()
    return full_text, extracted_images
