# task 01 == Розділіть змінну alice_in_wonderland так, щоб вона займала декілька фізичних ліній
alice_in_wonderland = (
    '"Would you tell me, please, which way I ought to go from here?"\n'
    '"That depends a good deal on where you want to get to," said the Cat.\n'
    '"I don\'t much care where ——" said Alice.\n'
    '"Then it doesn\'t matter which way you go," said the Cat.\n'
    '"—— so long as I get somewhere," Alice added as an explanation.\n'
    '"Oh, you\'re sure to do that," said the Cat, "if you only walk long enough."'
)

# task 02 == Знайдіть та відобразіть всі символи одинарної лапки (') у тексті
single_quotes = [ch for ch in alice_in_wonderland if ch == "'"]
print(f"task 02")
print(f"Кількість одинарних лапок:", len(single_quotes))
print(f"Символи:", single_quotes)
print()

# task 03 == Виведіть змінну alice_in_wonderland на друк
print(f"task 03")
print(alice_in_wonderland)
print()

# task 04
"""
Площа Чорного моря становить 436 402 км2, а площа Азовського
моря становить 37 800 км2. Яку площу займають Чорне та Азов-
ське моря разом?
"""

black_sea = 436402  # площа Чорного моря
azov_sea = 37800    # площа Азовського моря
total_area = black_sea + azov_sea

print(f"task 04")
print(f"Чорне та Азовське моря разом займають {total_area} км²")
print()


# task 05
"""
Мережа супермаркетів має 3 склади, де всього розміщено
375 291 товар. На першому та другому складах перебуває
250 449 товарів. На другому та третьому – 222 950 товарів.
Знайдіть кількість товарів, що розміщені на кожному складі.
"""

total_goods = 375_291      # всього товарів на 3 складах
first_plus_second = 250_449  # склад 1 + склад 2
second_plus_third = 222_950  # склад 2 + склад 3

# якщо додати всі три числа (загальна кількість, 1+2, 2+3),
# то склад 2 порахується двічі
warehouse_3 = total_goods - first_plus_second   # те, що лишилось - це 3 склад
warehouse_1 = total_goods - second_plus_third   # те, що лишилось - це 1 склад
warehouse_2 = first_plus_second - warehouse_1   # з першої суми віднімаємо 1 склад, отримуємо 2 склад

print("task 05")
print(f"На 1 складі: {warehouse_1} товарів")
print(f"На 2 складі: {warehouse_2} товарів")
print(f"На 3 складі: {warehouse_3} товарів")
print()


# task 06
"""
Михайло разом з батьками вирішили купити комп’ютер, ско-
риставшись послугою «Оплата частинами». Відомо, що сплачу-
вати необхідно буде півтора року по 1179 грн/місяць. Обчисліть
вартість комп’ютера.
"""

months = int(1.5 * 12)      # півтора роки = 1.5 * 12 місяців
price_per_month = 1179      # грн на місяць
computer_price = months * price_per_month

print("task 06")
print(f"Півтора роки = {months} місяців")
print(f"Вартість комп'ютера: {computer_price} грн")
print()


# task 07
"""
Знайди остачу від ділення чисел:
a) 8019 : 8     d) 7248 : 6
b) 9907 : 9     e) 7128 : 5
c) 2789 : 5     f) 19224 : 9
"""

pairs = [
    (8019, 8),
    (9907, 9),
    (2789, 5),
    (7248, 6),
    (7128, 5),
    (19224, 9),
]

print("task 07")
letters = "abcdef"
for letter, (a, b) in zip(letters, pairs):
    remainder = a % b
    print(f"{letter}) {a} : {b} = {remainder}")
print()


# task 08
"""
Іринка, готуючись до свого дня народження, склала список того,
що їй потрібно замовити. Обчисліть, скільки грошей знадобиться
для даного її замовлення.
Назва товару    Кількість   Ціна
Піца велика     4           274 грн
Піца середня    2           218 грн
Сік             4           35 грн
Торт            1           350 грн
Вода            3           21 грн
"""

order = [
    ("Піца велика", 4, 274),
    ("Піца середня", 2, 218),
    ("Сік", 4, 35),
    ("Торт", 1, 350),
    ("Вода", 3, 21),
]

print("task 08")
total_cost = 0
for name, quantity, price in order:
    cost = quantity * price
    total_cost = total_cost + cost
    print(f"{name}: {quantity} шт. x {price} грн = {cost} грн")

print(f"Загальна сума замовлення: {total_cost} грн")
print()


# task 09
"""
Ігор займається фотографією. Він вирішив зібрати всі свої 232
фотографії та вклеїти в альбом. На одній сторінці може бути
розміщено щонайбільше 8 фото. Скільки сторінок знадобиться
Ігорю, щоб вклеїти всі фото?
"""

import math

photos = 232
photos_per_page = 8
pages = math.ceil(photos / photos_per_page)

print("task 09")
print(f"Ігорю знадобиться {pages} сторінок для {photos} фотографій")
print()


# task 10
"""
Родина зібралася в автомобільну подорож із Харкова в Буда-
пешт. Відстань між цими містами становить 1600 км. Відомо,
що на кожні 100 км необхідно 9 літрів бензину. Місткість баку
становить 48 літрів.
1) Скільки літрів бензину знадобиться для такої подорожі?
2) Скільки щонайменше разів родині необхідно заїхати на зап-
равку під час цієї подорожі, кожного разу заправляючи пов-
ний бак?
"""

distance = 1600      # км
fuel_per_100km = 9   # росхід літрів на 100 км
tank_capacity = 48   # ємність баку в літрах

total_fuel = (distance / 100) * fuel_per_100km
# скільки разів потрібно заправитись повним баком,
# якщо на старті бак вже повний
refuels_needed = math.ceil(total_fuel / tank_capacity) - 1  #-1 тому що на старті повний бак

print("task 10")
print(f"1) Для подорожі знадобиться {total_fuel:.0f} літрів бензину")
print(f"2) Родині потрібно щонайменше {refuels_needed} рази заїхати на заправку "
      f"(якщо на старті бак повний)")