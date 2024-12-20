from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from pathlib import Path

def adjust_brightness(image, factor=1.3):
    """Meningkatkan kecerahan gambar sebesar 30%."""
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def resize_image(image, size=(300, 300)):
    """Mengubah ukuran gambar menjadi ukuran tertentu dengan resampling."""
    return image.resize(size, Image.Resampling.LANCZOS)

def add_border(image, border_width=10, border_color='black'):
    """Menambahkan border pada gambar."""
    return ImageOps.expand(image, border_width, fill=border_color)

def sharpen_image(image):
    """Memperjelas gambar."""
    return image.filter(ImageFilter.SHARPEN)

def convert_to_grayscale(image):
    """Mengubah gambar menjadi grayscale."""
    return ImageOps.grayscale(image)

def add_watermark(image, watermark_text="Watermark", font_size=20):
    """Menambahkan watermark dalam kotak di kanan atas gambar."""
    image_copy = image.copy()  # membuat salinan image supaya gambar asli tidak berubah (immutable)
    draw = ImageDraw.Draw(image_copy)
    font = ImageFont.load_default()  # Menggunakan font default

    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Menentukan posisi kotak watermark di kanan atas
    margin = 10
    box_x1 = image_copy.width - margin
    box_y0 = margin
    box_x0 = box_x1 - text_width - 2 * margin
    box_y1 = box_y0 + text_height + 2 * margin

    # Menambahkan kotak
    draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill="white", outline="black")

    # Menambahkan teks watermark
    text_x = box_x0 + margin
    text_y = box_y0 + margin
    draw.text((text_x, text_y), watermark_text, fill="black", font=font)

    return image_copy

def process_image_logic(image, watermark_text="toko pak ronaldo"):
    """Pipeline proses gambar tanpa efek samping."""
    image = adjust_brightness(image)
    image = resize_image(image)
    image = add_border(image)
    image = sharpen_image(image)
    image = add_watermark(image, watermark_text=watermark_text)
    image_gray = convert_to_grayscale(image)
    return image, image_gray

def process_image_io(image_path, output_dir, watermark_text="toko pak ronaldo"):
    """Fungsi dengan efek samping untuk membaca, menyimpan, dan menampilkan gambar."""
    image = Image.open(image_path)
    edited_image, grayscale_image = process_image_logic(image, watermark_text)

    # Membuat output directory jika belum ada
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Menyimpan gambar hasil edit
    output_path = Path(output_dir) / f"edited_{Path(image_path).name}"
    edited_image.save(output_path)

    return edited_image, grayscale_image, str(output_path)

def process_directory(input_dir, output_dir, watermark_text="toko pak ronaldo"):
    """Memproses semua gambar di direktori input."""
    input_path = Path(input_dir)
    if not input_path.is_dir():
        raise ValueError(f"Input path '{input_dir}' is not a valid directory.")

    for image_path in input_path.glob('*.png'):
        edited_image, grayscale_image, edited_image_path = process_image_io(
            str(image_path), output_dir, watermark_text
        )
        compare_images(str(image_path), edited_image_path, grayscale_image)

def compare_images(original_path, edited_image_path, grayscale_image):
    """Membandingkan gambar asli, hasil edit, dan hasil grayscale."""
    original_image = Image.open(original_path)

    # Menyiapkan subplot
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # Menampilkan gambar asli, hasil edit, dan grayscale
    axs[0].imshow(original_image)
    axs[0].set_title('Original Image')
    axs[0].axis('off')

    edited_image = Image.open(edited_image_path)
    axs[1].imshow(edited_image)
    axs[1].set_title('Edited Image')
    axs[1].axis('off')

    axs[2].imshow(grayscale_image, cmap='gray')
    axs[2].set_title('Grayscale Image')
    axs[2].axis('off')

    plt.show()

def main(input_dir, output_dir, watermark_text="toko pak ronaldo"):
    """Fungsi utama untuk menjalankan seluruh proses."""
    process_directory(input_dir, output_dir, watermark_text)

# Contoh penggunaan
input_dir = 'image'  # Direktori untuk gambar baju
output_dir = 'edited_images'  # Direktori untuk menyimpan hasil edit
main(input_dir, output_dir)
