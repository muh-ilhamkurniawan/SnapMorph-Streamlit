import streamlit as st
from rembg import remove
from PIL import Image, ImageChops
import io

def remove_bg_page():
    st.header("Remove Background from Image")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Original Image', use_column_width=True)

        output_image = remove(image)
        st.image(output_image, caption='Image with Background Removed', use_column_width=True)

        # Choose format for saving
        file_format = st.selectbox("Choose file format to save", ["PNG", "JPG", "JPEG", "PDF"])

        # Save and download button
        buf = io.BytesIO()
        if file_format in ["JPG", "JPEG"]:
            output_image = output_image.convert("RGB")
        output_image.save(buf, format=file_format)
        byte_im = buf.getvalue()

        st.download_button(label="Download Image",
                           data=byte_im,
                           file_name=f"output.{file_format.lower()}",
                           mime=f"image/{file_format.lower()}")

def change_bg_color_page():
    st.header("Change Background Color of Image")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Original Image', use_column_width=True)

        output_image = remove(image)

        bg_color = st.color_picker("Pick a background color", "#ffffff")
        bg_image = Image.new("RGBA", output_image.size, bg_color)
        final_image = Image.alpha_composite(bg_image, output_image.convert("RGBA"))

        st.image(final_image, caption='Image with New Background Color', use_column_width=True)

        # Choose format for saving
        file_format = st.selectbox("Choose file format to save", ["PNG", "JPG", "JPEG", "PDF"])

        # Save and download button
        buf = io.BytesIO()
        if file_format in ["JPG", "JPEG"]:
            final_image = final_image.convert("RGB")
        if file_format == "PDF":
            final_image.save(buf, format="PNG")
            final_image = Image.open(buf)
            buf = io.BytesIO()  # Clear the buffer
            final_image.save(buf, format="PDF")
        else:
            final_image.save(buf, format=file_format)
        byte_im = buf.getvalue()

        st.download_button(label="Download Image",
                           data=byte_im,
                           file_name=f"output_with_bg.{file_format.lower()}",
                           mime=f"image/{file_format.lower()}")

# Main app structure
st.sidebar.title("App Navigation")
page = st.sidebar.radio("Go to", ["Remove Background", "Change Background Color"])
st.title("Custom Background")
if page == "Remove Background":
    remove_bg_page()
elif page == "Change Background Color":
    change_bg_color_page()
