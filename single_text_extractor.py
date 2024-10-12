import os
from google.cloud import vision
import io

# Set the environment variable to the path of your JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"absolute-realm-438217-v5-b39115af94aa.json"

def detect_text(image_path):
    """Detects text in the image."""
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts  # Return the texts for further processing
    else:
        print(f'No text found in {image_path}.')
        return []

def get_largest_text(texts):
    """Finds the largest text based on bounding box area."""
    largest_area = 0
    largest_text = None

    for text in texts[1:]:  # Skip the first element, which is the full text
        bounding_poly = text.bounding_poly

        # Calculate the area of the bounding polygon
        width = bounding_poly.vertices[2].x - bounding_poly.vertices[0].x
        height = bounding_poly.vertices[2].y - bounding_poly.vertices[0].y
        area = abs(width * height)

        if area > largest_area:
            largest_area = area
            largest_text = text.description

    return largest_text

def process_images_in_folder(folder_path):
    """Processes all images in a folder and saves the output in Brands/image_name.txt."""
    # Ensure the output folder exists
    output_folder = os.path.join("Brands")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the folder
    for image_file in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_file)
        
        # Detect text in the image
        texts = detect_text(image_path)
        if texts:
            # Get the largest text (if needed)
            largest_text = get_largest_text(texts)
            if largest_text:
                # Save the output to a text file with UTF-8 encoding
                output_file = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"Brand name: {largest_text}\n")
                    f.write("Detected texts:\n")
                    # Only print and save the first element (full block of text)
                    f.write(f'{texts[0].description}\n')
                
                print(f"Processed {image_file}, brand name saved in {output_file}")
            else:
                print(f"No large text found in {image_file}")
        else:
            print(f"No text found in {image_file}")

if __name__ == "__main__":
    folder_path = r"OCRData/images"  # Folder containing the images
    process_images_in_folder(folder_path)
