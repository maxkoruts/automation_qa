import struct
import sys
import zlib

import requests

BASE_URL = 'http://127.0.0.1:8080'


def create_png(width=64, height=64, color=(255, 0, 0)):
    """Створює однотонне PNG-зображення (без зовнішніх бібліотек)."""

    def make_chunk(chunk_type, data):
        # Кожен блок PNG: довжина + тип + дані + контрольна сума CRC
        body = chunk_type + data
        crc = zlib.crc32(body) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + body + struct.pack('>I', crc)

    # Кожен рядок починається з байта фільтра (0), далі йдуть пікселі RGB
    row = b'\x00' + bytes(color) * width
    pixel_data = zlib.compress(row * height)

    # Заголовок: ширина, висота, глибина 8 біт, тип кольору 2 (RGB)
    header = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)

    return (
        b'\x89PNG\r\n\x1a\n'  # сигнатура PNG
        + make_chunk(b'IHDR', header)
        + make_chunk(b'IDAT', pixel_data)
        + make_chunk(b'IEND', b'')
    )


def main():
    # Можна передати шлях до власного зображення: python client.py photo.png
    if len(sys.argv) > 1:
        path = sys.argv[1]
        filename = path.replace('\\', '/').split('/')[-1]
        with open(path, 'rb') as f:
            content = f.read()
    else:
        filename = 'test_image.png'
        content = create_png()

    # 1. POST /upload: завантаження зображення (поле форми має називатися 'image')
    response = requests.post(
        f'{BASE_URL}/upload',
        files={'image': (filename, content)},
    )
    print('POST /upload  ->', response.status_code, response.json())
    response.raise_for_status()

    # 2. GET /image/<filename>: отримання посилання (Content-Type: text)
    response = requests.get(
        f'{BASE_URL}/image/{filename}',
        headers={'Content-Type': 'text'},
    )
    print('GET  /image   ->', response.status_code, response.json())
    response.raise_for_status()
    print('Посилання на файл:', response.json()['image_url'])

    # 3. DELETE /delete/<filename>: видалення файлу
    response = requests.delete(f'{BASE_URL}/delete/{filename}')
    print('DELETE /delete ->', response.status_code, response.json())
    response.raise_for_status()

    # 4. Перевірка: GET має повернути 404, бо файл видалено
    response = requests.get(
        f'{BASE_URL}/image/{filename}',
        headers={'Content-Type': 'text'},
    )
    print('GET  /image (перевірка) ->', response.status_code, response.json())
    if response.status_code == 404:
        print('Зображення успішно видалене з сервера.')
    else:
        print('Помилка: зображення все ще існує!')


if __name__ == '__main__':
    main()