import requests

BASE_URL = "https://images-api.nasa.gov"

# 1. Пошук зображень
search_url = f"{BASE_URL}/search"
search_params = {
    "q": "Curiosity rover Mars",
    "media_type": "image",
    "page_size": 20,
}

# Шаблон для отримання файлів по nasa_id
asset_url_template = f"{BASE_URL}/asset/{{nasa_id}}"


def pick_best_jpg(urls):
    """Обирає "найкращий" JPG зі списку URL.

    Пріоритет: orig > large > medium > small > thumb > будь-який інший .jpg
    """
    jpgs = [u for u in urls if u.lower().endswith((".jpg", ".jpeg"))]
    if not jpgs:
        return None

    for suffix in ("~orig", "~large", "~medium", "~small", "~thumb"):
        for url in jpgs:
            if suffix in url.lower():
                return url
    return jpgs[0]


def download_file(url, filename):
    """Скачує файл за URL і зберігає його локально."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Збережено {filename} ({len(response.content) / 1024:.1f} КБ)")


def main():
    # Запит 1: пошук
    response = requests.get(search_url, params=search_params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # 2. Витягуємо nasa_id з відповіді
    items = data["collection"]["items"]
    nasa_ids = [
        item["data"][0]["nasa_id"]
        for item in items
        if item.get("data")
    ]
    print(f"Знайдено {len(nasa_ids)} елементів")

    # 3-4. Для кожного nasa_id запитуємо /asset і обираємо JPG
    saved = 0
    for nasa_id in nasa_ids:
        if saved == 2:
            break

        asset_url = asset_url_template.format(nasa_id=nasa_id)
        asset_response = requests.get(asset_url, timeout=30)
        asset_response.raise_for_status()
        asset_data = asset_response.json()

        urls = [entry["href"] for entry in asset_data["collection"]["items"]]
        jpg_url = pick_best_jpg(urls)

        print(f"[{nasa_id}] Обрано: {jpg_url}")

        # 5. Скачуємо зображення
        saved += 1
        download_file(jpg_url, f"mars_photo{saved}.jpg")


if __name__ == "__main__":
    main()