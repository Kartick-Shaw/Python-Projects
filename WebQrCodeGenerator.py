import qrcode
from PIL import Image
import streamlit as st
import io

st.title("QR Code Generator")

text = st.text_input("Enter your text: ")
generate = st.button('Generate')

if generate and text:
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the PIL Image to a BytesIO buffer and convert it to bytes
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_bytes = img_buffer.getvalue()

    # Display the Qr Code
    st.text("Scan the QR Code")
    st.image(img_bytes, width=400)
    
    # Download Button to Download the image
    st.download_button(
        label='Download',
        key='qr_code_download',
        data=img_bytes,
        file_name='QR_Code.png',
        mime='image/png'
    )