# main.py
from image_tools import *  # image_tools.py'daki tüm fonksiyonları içe aktar

#act1
def lzw_compress(data):
    dictionary = {chr(i): i for i in range(256)}
    current_code = 256
    result = []
    w = ''

    for pixel in data:
        wc = w + pixel
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = current_code
            current_code += 1
            w = pixel

    if w:
        result.append(dictionary[w])
    return result, dictionary

#act2 convert two bit binary format string experssion
def to_binary(data, codelength=12):
    return ''.join(format(code, f'0{codelength}b') for code in data)

#act3 calculate
def entropy(data):
    value, counts = np.unique(data, return_counts=True)
    norm_counts = counts / counts.sum()
    return -(norm_counts * np.log2(norm_counts)).sum()
def compression_ratio(original_size, compressed_size):
    return original_size / compressed_size


# split image r, g, b
img = readPILimg('image.jpg')
r_gray = np.array(red_values(img))
g_gray = np.array(green_values(img))
b_gray = np.array(blue_values(img))

# compreseed data and new dict
r_compressed, r_dict = lzw_compress(r_gray.flatten())
g_compressed, g_dict = lzw_compress(g_gray.flatten())
b_compressed, b_dict = lzw_compress(b_gray.flatten())

# binary format from string
r_bin = to_binary(r_compressed)
g_bin = to_binary(g_compressed)
b_bin = to_binary(b_compressed)

# save
with open('compressed_image.bin', 'w') as f:
    f.write(r_bin + g_bin + b_bin) # 2 li byte dizileriin birleştirme ve kayıt eme

# 5. Entropi hesaplama
entropy_r = entropy(r_compressed)
entropy_g = entropy(g_compressed)
entropy_b = entropy(b_compressed)

print(f"Red Entropy: {entropy_r:.4f}")
print(f"Green Entropy: {entropy_g:.4f}")
print(f"Blue Entropy: {entropy_b:.4f}")

# 6. Dosya boyutu ve sıkıştırma oranı
original_size = img.size[0] * img.size[1] * 24  # 24 bit (RGB) için orijinal boyut
compressed_size = len(r_bin) + len(g_bin) + len(b_bin)  # ikili verinin toplam boyutu
compression_ratio_value = compression_ratio(original_size, compressed_size)

print(f"Original Size: {original_size} bits")
print(f"Compressed Size: {compressed_size} bits")
print(f"Compression Ratio: {compression_ratio_value:.4f}")

# 7. Dosyadan sıkıştırılmış veriyi okuma
with open('compressed_image.bin', 'r') as f:
    compressed_data = f.read()

# RGB bileşenlerine ayırma
r_bin, g_bin, b_bin = compressed_data[:len(r_bin)], compressed_data[len(r_bin):2 * len(r_bin)], compressed_data[
                                                                                                2 * len(r_bin):]


# 8. LZW geri sıkıştırma fonksiyonu
def lzw_decompress(data, dictionary):
    reverse_dict = {v: k for k, v in dictionary.items()}
    w = reverse_dict[data[0]]
    result = [w]
    for code in data[1:]:
        if code in reverse_dict:
            entry = reverse_dict[code]
        else:
            entry = w + w[0]
        result.append(entry)
        reverse_dict[len(reverse_dict)] = w + entry[0]
        w = entry
    return result


# Geri sıkıştırılmış verileri çözme
r_decompressed = lzw_decompress(r_compressed, r_dict)
g_decompressed = lzw_decompress(g_compressed, g_dict)
b_decompressed = lzw_decompress(b_compressed, b_dict)

# Veriyi yeniden şekillendirme
r_restored = np.array(r_decompressed).reshape(r_gray.shape)
g_restored = np.array(g_decompressed).reshape(g_gray.shape)
b_restored = np.array(b_decompressed).reshape(b_gray.shape)

# RGB'ye dönüştürme ve yeniden oluşturulan görüntüyü kaydetme
restored_image = merge_image(arr_to_PIL(r_restored), arr_to_PIL(g_restored), arr_to_PIL(b_restored))
restored_image.save('restored_image.jpg')
