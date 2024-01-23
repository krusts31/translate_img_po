from PIL import Image
import pytesseract

# Function to perform OCR on an image file and return the text
def image_to_text(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img, lang='nld')
        
    return text

# Example usage:
image_path = 'img/PHOTO-2023-12-31-19-57-28.jpg'

extracted_text = image_to_text(image_path)
print(extracted_text)
