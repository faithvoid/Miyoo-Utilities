from PIL import Image, ImageOps
import sys
import io
import os

def process_image(input_path, output_path="image1.jpg", target_size=(640, 480), max_size_kb=115):
    img = Image.open(input_path)

    img = ImageOps.mirror(img)
    img = ImageOps.flip(img)

    if img.size != target_size:
        img = img.resize(target_size, Image.LANCZOS)

    img = img.convert("RGB")

    low, high = 10, 95
    best_quality = low
    best_data = None

    while low <= high:
        mid = (low + high) // 2
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=mid, optimize=True)
        size_kb = len(buffer.getvalue()) / 1024

        if size_kb <= max_size_kb:
            best_quality = mid
            best_data = buffer.getvalue()
            low = mid + 1
        else:
            high = mid - 1

    if best_data:
        with open(output_path, "wb") as f:
            f.write(best_data)
        print(f"Saved '{output_path}' at quality={best_quality}, size={len(best_data)/1024:.2f} KB")
    else:
        print("Could not compress image under size limit (even at quality=10).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python img2boot.py input.jpg")
    else:
        process_image(sys.argv[1])
