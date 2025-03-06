from PIL import Image
import numpy as np

#act 1
img = Image.open('image.jpg')
img_rgb = img.convert('RGB')

r, g, b = img_rgb.split()

r_gray = np.array(r)
g_gray = np.array(g)
b_gray = np.array(b)

#act2
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

r_compressed, r_dict = lzw_compress(r_gray.flatten())
g_compressed, g_dict = lzw_compress(g_gray.flatten())
b_compressed, b_dict = lzw_compress(b_gray.flatten())


#act3
def to_binary(data):
    return ''.join(format(code, '016b') for code in data)  # 16 bitlik ikili koda çevir

r_bin = to_binary(r_compressed)
g_bin = to_binary(g_compressed)
b_bin = to_binary(b_compressed)

#act4
with open('compressed_image.bin', 'w') as f:
    f.write(r_bin + g_bin + b_bin)

#act5 average, calculate


#act 6 convert data
with open('compressed_image.bin', 'r') as f:
    compressed_data = f.read()

# Sıkıştırılmış veriyi RGB bileşenlerine ayır
r_bin, g_bin, b_bin = compressed_data[:len(r_bin)], compressed_data[len(r_bin):2*len(r_bin)], compressed_data[2*len(r_bin):]

#act 7
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

r_decompressed = lzw_decompress(r_compressed, r_dict)
g_decompressed = lzw_decompress(g_compressed, g_dict)
b_decompressed = lzw_decompress(b_compressed, b_dict)

#act 8
r_restored = np.array(r_decompressed).reshape(r_gray.shape)
g_restored = np.array(g_decompressed).reshape(g_gray.shape)
b_restored = np.array(b_decompressed).reshape(b_gray.shape)

# RGB'ye dönüştür ve geri yüklenen görüntüyü oluştur
restored_image = Image.merge('RGB', (Image.fromarray(r_restored), Image.fromarray(g_restored), Image.fromarray(b_restored)))
restored_image.save('image.jpg')
