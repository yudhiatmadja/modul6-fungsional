from PIL import Image, ImageEnhance 

image_path = 'image/gkb.jpg'  

img = Image.open(image_path)  

    # 2. Tingkatkan saturasi
enhancer = ImageEnhance.Color(img)  # Buat objek enhancer untuk manipulasi saturasi warna gambar
enhanced_img = enhancer.enhance(3.2)  # Tingkatkan saturasi warna gambar 2.5 kali (nilai > 1 untuk lebih cerah)

    # 3. Tingkatkan kecerahan
brightness_enhancer = ImageEnhance.Brightness(enhanced_img)  # Buat objek enhancer untuk manipulasi kecerahan gambar
bright_img = brightness_enhancer.enhance(1.6)  # Tingkatkan kecerahan gambar 1.2 kali (nilai > 1 lebih cerah)

# 4. Tingkatkan ketajaman
sharpness_enhancer = ImageEnhance.Sharpness(bright_img)  # Buat objek enhancer untuk manipulasi ketajaman gambar
sharp_img = sharpness_enhancer.enhance(2.3)  # Tingkatkan ketajaman gambar (nilai > 1 untuk lebih tajam)

# 5. Potong gambar untuk zoom in
width, height = img.size  # Ambil ukuran gambar dalam piksel (lebar dan tinggi)
left = width * 0.0# Titik mulai crop sisi kiri (10% dari lebar)
top = height * 0.1# Titik mulai crop sisi atas (10% dari tinggi)
right = width * 0.65 # Titik akhir crop sisi kanan (70% dari lebar gambar)
bottom = height * 0.85# Titik akhir crop sisi bawah (70% dari tinggi gambar)

zoom_img = sharp_img.crop((left, top, right, bottom))  # Crop bagian tengah gambar sebagai hasil zoom

zoom_img.save('result/image_result.png')
zoom_img.show()
