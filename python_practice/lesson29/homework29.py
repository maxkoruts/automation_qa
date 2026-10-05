from playwright.sync_api import sync_playwright

def check_installation():
    with sync_playwright() as p:
        # Запускаємо браузер у headless режимі
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Відкриваємо сторінку Playwright
        page.goto("https://playwright.dev/python")

        # Отримуємо та виводимо заголовок
        title = page.title()
        print(f"Заголовок сторінки:{title}")

        browser.close()

if __name__ == "__main__":
    check_installation()