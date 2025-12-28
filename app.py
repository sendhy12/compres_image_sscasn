import streamlit as st
from PIL import Image
from io import BytesIO

MAX_SIZE_KB = 200

def compress_image(image, max_size_kb=200):
    img = image.convert("RGB")
    quality = 95
    buffer = BytesIO()

    # Kompresi dengan menurunkan kualitas
    while quality > 10:
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        size_kb = buffer.tell() / 1024

        if size_kb <= max_size_kb:
            return buffer, size_kb

        quality -= 5

    # Jika masih besar, lakukan resize
    width, height = img.size
    while True:
        width = int(width * 0.9)
        height = int(height * 0.9)
        img = img.resize((width, height), Image.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=70)
        size_kb = buffer.tell() / 1024

        if size_kb <= max_size_kb or width < 300:
            return buffer, size_kb


st.set_page_config(page_title="Image Compressor", layout="centered")

st.title("📷 Kompresi Gambar Maksimal 200 KB")
st.write("Unggah gambar, sistem akan mengompresi otomatis hingga ukuran ≤ 200 KB.")

uploaded_file = st.file_uploader(
    "Unggah gambar (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    original_image = Image.open(uploaded_file)
    original_size_kb = uploaded_file.size / 1024

    st.subheader("Gambar Asli")
    st.image(original_image, use_container_width=True)
    st.write(f"Ukuran asli: **{original_size_kb:.2f} KB**")

    if st.button("Kompres Gambar"):
        compressed_buffer, final_size_kb = compress_image(
            original_image, MAX_SIZE_KB
        )

        st.subheader("Hasil Kompresi")
        st.image(
            Image.open(compressed_buffer),
            use_container_width=True
        )
        st.write(f"Ukuran setelah kompresi: **{final_size_kb:.2f} KB**")

        st.download_button(
            label="Unduh Gambar Terkompresi",
            data=compressed_buffer.getvalue(),
            file_name="compressed_image.jpg",
            mime="image/jpeg"
        )
