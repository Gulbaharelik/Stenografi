# GEREKLİ KÜTÜPHANE

from PIL import Image
import os

# METİN <-> BİT DÖNÜŞÜMÜ

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

# ENCODE

def encode_image(input_image, output_image, secret_text):
    img = Image.open(input_image)
    img = img.convert("RGB")

    binary_text = text_to_binary(secret_text) + '1111111111111110'
    data_index = 0

    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            if data_index < len(binary_text):
                r, g, b = pixels[x, y]

                r = (r & ~1) | int(binary_text[data_index])
                data_index += 1

                if data_index < len(binary_text):
                    g = (g & ~1) | int(binary_text[data_index])
                    data_index += 1

                if data_index < len(binary_text):
                    b = (b & ~1) | int(binary_text[data_index])
                    data_index += 1

                pixels[x, y] = (r, g, b)
            else:
                break

    img.save(output_image)
    print(f"[+] Mesaj gizlendi -> {output_image}")


# DECODE

def decode_image(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")

    pixels = img.load()
    binary_data = ""

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    end_marker = "1111111111111110"
    if end_marker in binary_data:
        binary_data = binary_data[:binary_data.index(end_marker)]

    message = binary_to_text(binary_data)
    print("[+] Gizli mesaj:")
    print(message)


# CLI (KOMUT SATIRI ARAYÜZÜ)

def menu():
    print("\n------------------------ Steganografi Uygulaması--------------------------")
    print("1 - Mesaj Gizle (Encode)")
    print("2 - Mesaj Çıkar (Decode)")

    choice = input("Seçiminiz (1-2): ")

    if choice == "1":
        input_image = input("Görsel dosya yolu (örn: deneme.png): ")
        
        if not os.path.exists(input_image):
            print("Dosya bulunamadı!")
            return

        text = input("Gizlenecek mesajı yaz: ")

        encode_image(input_image, "cikti.png", text)

        print("\nÇıktı kaydedildi: cikti.png")

    elif choice == "2":
        image = input("Mesaj içeren görsel dosya yolu: ")
        
        if not os.path.exists(image):
            print("Dosya bulunamadı!")
            return

        decode_image(image)

    else:
        print("Geçersiz seçim!")

# PROGRAMI BAŞLAT
menu()
