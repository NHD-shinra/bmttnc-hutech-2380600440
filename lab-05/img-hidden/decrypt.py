import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""

    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))

            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]

    message = ""
    for i in range(0, len(binary_message), 8):
        byte_chunk = binary_message[i:i+8]
        if len(byte_chunk) < 8:
            break
            
        val = int(byte_chunk, 2)
        char = chr(val)
        
        # XÁO TRỘN KÝ TỰ RÁC: Kết hợp chỉ số i để tạo ra các ký tự ngẫu nhiên khác nhau
        if val < 32 or val == 127:
            char = chr(((val + i + 37) % 94) + 33)
            
        message += char
        
        if message.endswith("ÿþ"):
            break
            
        if len(message) >= 30:
            break

    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()