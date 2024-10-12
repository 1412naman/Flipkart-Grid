import os
from google.cloud import vision
import io
import re

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
        return texts[0].description  # Return the full block of text
    else:
        print(f'No text found in {image_path}.')
        return ''

def extract_mfg_exp_dates(text):
    """Extracts the first and second dates found in the text as MFG and EXP dates."""
    # Regular expression to match date patterns
    date_pattern = r'\b(\d{2}\/\d{2}\/\d{4}|\d{2}\/\d{2}\/\d{2}|\d{2}-\d{2}-\d{4}|\d{2}-\d{2}-\d{2})\b'
    
    # Find all dates in the text
    dates = re.findall(date_pattern, text)
    
    if len(dates) >= 2:
        mfg_date = dates[0]
        exp_date = dates[1]
        return mfg_date, exp_date
    elif len(dates) == 1:
        mfg_date = dates[0]
        return mfg_date, "Expiry date not found"
    else:
        return "Manufacturing date not found", "Expiry date not found"

def process_images_in_folder(folder_path):
    """Processes all images in a folder and saves the output in Brands/image_name.txt."""
    # Ensure the output folder exists
    output_folder = os.path.join("BackDetails")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the folder
    for image_file in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_file)
        
        # Detect text in the image
        full_text = detect_text(image_path)
        if full_text:
            # Extract the MFG and EXP dates from the detected text
            mfg_date, exp_date = extract_mfg_exp_dates(full_text)

            # Save the output to a text file with UTF-8 encoding
            output_file = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                # f.write(f"Detected Text:\n{full_text}\n")
                f.write(f"\nMFG Date: {mfg_date}\n")
                f.write(f"EXP Date: {exp_date}\n")
                
            print(f"Processed {image_file}, MFG and EXP dates saved in {output_file}")
        else:
            print(f"No text found in {image_file}")

if __name__ == "__main__":
    folder_path = r"OCRData/test_imgs"  # Folder containing the images
    process_images_in_folder(folder_path)
