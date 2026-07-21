# ==========================================
# تمرین ۱: مخفی‌سازی تصویر با 2-Bit LSB
# ==========================================

from PIL import Image
import matplotlib.pyplot as plt

# ------------------------------------------
# بخش ۱: مخفی‌سازی تصویر (Embed - 2 Bit)
# ------------------------------------------
def hide_image_2bit(cover_path, secret_path, output_path):
    cover = Image.open(cover_path)
    secret = Image.open(secret_path).resize(cover.size)

    cover_pixels = cover.load()
    secret_pixels = secret.load()

    for x in range(cover.width):
        for y in range(cover.height):
            r_c, g_c, b_c = cover_pixels[x, y]
            r_s, g_s, b_s = secret_pixels[x, y]

            # حذف 2 بیت آخر و جایگزینی با 2 بیت تصویر مخفی
            r = (r_c & 0xFC) | (r_s >> 6)
            g = (g_c & 0xFC) | (g_s >> 6)
            b = (b_c & 0xFC) | (b_s >> 6)

            cover_pixels[x, y] = (r, g, b)

    cover.save(output_path)
    print("✅ تصویر مخفی شده (2-bit) ذخیره شد:", output_path)

    plt.imshow(cover)
    plt.title("Stego Image (2-bit LSB)")
    plt.axis("off")
    plt.show()


# ------------------------------------------
# بخش ۲: استخراج تصویر مخفی (Extract - 2 Bit)
# ------------------------------------------
def extract_image_2bit(stego_path, output_path):
    stego = Image.open(stego_path)
    width, height = stego.size
    stego_pixels = stego.load()

    secret = Image.new("RGB", stego.size)
    secret_pixels = secret.load()

    for x in range(width):
        for y in range(height):
            r, g, b = stego_pixels[x, y]

            # استخراج 2 بیت و بازسازی شدت رنگ
            r_s = (r & 0x03) << 6
            g_s = (g & 0x03) << 6
            b_s = (b & 0x03) << 6

            secret_pixels[x, y] = (r_s, g_s, b_s)

    secret.save(output_path)
    print("✅ تصویر مخفی استخراج شد (2-bit):", output_path)

    plt.imshow(secret)
    plt.title("Extracted Secret Image (2-bit)")
    plt.axis("off")
    plt.show()


# ------------------------------------------
# اجرای برنامه
# ------------------------------------------
hide_image_2bit("cover.jpg", "secret.jpg", "stego_2bit.png")
extract_image_2bit("stego_2bit.png", "extracted_secret_2bit.png")
