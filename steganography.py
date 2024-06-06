import streamlit as st
from PIL import Image
import io

def encode_image(img, message):
    encoded = img.copy()
    width, height = img.size

    # Convert message to binary
    binary_message = ''.join(format(ord(i), '08b') for i in message)
    binary_message += '1111111111111110'  # Delimiter to indicate end of the message

    data_index = 0
    binary_message_length = len(binary_message)
    
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for n in range(3):  # Iterate through RGB
                if data_index < binary_message_length:
                    pixel[n] = pixel[n] & ~1 | int(binary_message[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= binary_message_length:
                break
        if data_index >= binary_message_length:
            break
    
    return encoded

def decode_image(image):
    width, height = image.size

    binary_message = ''
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for n in range(3):  # Iterate through RGB
                binary_message += str(pixel[n] & 1)
    
    all_bytes = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''
    for byte in all_bytes:
        decoded_message += chr(int(byte, 2))
        if decoded_message[-2:] == '~~':  # Check for delimiter
            break

    return decoded_message[:-2]

def main():
    st.title("Steganography App")
    st.write("Encode and Decode messages in images")

    option = st.selectbox("Choose an option", ("Encode", "Decode"))

    if option == "Encode":
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            img = Image.open(uploaded_image)
            st.image(img, caption='Uploaded Image', use_column_width=True)
            message = st.text_area("Enter the message to encode")
            if st.button("Encode"):
                encoded_img = encode_image(img, message)
                buf = io.BytesIO()
                encoded_img.save(buf, format='PNG')
                byte_im = buf.getvalue()
                st.download_button("Download Encoded Image", data=byte_im, file_name="encoded_image.png", mime="image/png")
                st.image(encoded_img, caption='Encoded Image', use_column_width=True)

    elif option == "Decode":
        uploaded_image = st.file_uploader("Upload an image to decode", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            img = Image.open(uploaded_image)
            st.image(img, caption='Uploaded Image', use_column_width=True)
            if st.button("Decode"):
                decoded_message = decode_image(img)
                st.write("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()
