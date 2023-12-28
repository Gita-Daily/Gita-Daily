from PIL import Image
import cv2
import os

def get_file_size(file_path):
    return os.path.getsize(file_path)

def reduce_file_size(image_path, output_path, target_size_mb=5):
    # Load the image using PIL
    img = Image.open(image_path)

    # Convert to JPEG (For better compression)
    img = img.convert("RGB")
    
    # Step 1: Reduce resolution
    # base_width = 800
    # w_percent = (base_width / float(img.size[0]))
    # h_size = int((float(img.size[1]) * float(w_percent)))
    # img = img.resize((base_width, h_size), Image.ANTIALIAS)

    # Step 2: Compression
    img.save(output_path, "JPEG", quality=85)  # You can change quality to a lower value for higher compression
    
    # Check file size
    file_size_kb = get_file_size(output_path) / 1024.0
    file_size_mb = file_size_kb / 1024.0

    # Step 3 & 4: Use OpenCV for additional compression techniques if needed
    if file_size_mb > target_size_mb:
        img_cv = cv2.imread(output_path)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]  # You can change to a lower value
        cv2.imwrite(output_path, img_cv, encode_param)

    # Final size check
    file_size_kb = get_file_size(output_path) / 1024.0
    file_size_mb = file_size_kb / 1024.0
    if file_size_mb > target_size_mb:
        print(f"Failed to reduce the file size below {target_size_mb}MB.")
    else:
        print(f"Success! The reduced file size is {file_size_mb:.2f}MB.")

if __name__ == "__main__":
    image_path = "/Users/blackhole/Downloads/2.png"  # Replace with your image path
    output_path = "output.jpg"  # The path for the reduced image
    reduce_file_size(image_path, output_path)
