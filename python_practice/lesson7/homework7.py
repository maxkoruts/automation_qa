# task 1
""" Задача - надрукувати табличку множення на задане число, але
лише до максимального значення для добутку - 25.
Код майже готовий, треба знайти помилки та випраавити\доповнити.
"""
print("task1")
def multiplication_table(number):
    # Initialize the appropriate variable
    multiplier = 1

    # Complete the while loop condition.
    while True:
        result = number * multiplier
        if result > 25:
            # Enter the action to take if the result is greater than 25
            break
        print(str(number) + "x" + str(multiplier) + "=" + str(result))

        # Increment the appropriate variable
        multiplier += 1

multiplication_table(3)
# Should print:
# 3x1=3
# 3x2=6
# 3x3=9
# 3x4=12
# 3x5=15
print()

# task 2
"""  Написати функцію, яка обчислює суму двох чисел.
"""
print("task2")
def sum_two_numbers(a, b):
    return a + b
print(sum_two_numbers(3, 5))
print()

# task 3
"""  Написати функцію, яка розрахує середнє арифметичне списку чисел.
"""
print("task3")
def average(numbers):
    return sum(numbers) / len(numbers)
print(average([1, 2, 3, 4, 5]))
print()

# task 4
"""  Написати функцію, яка приймає рядок та повертає його у зворотному порядку.
"""
print("task4")
def reverse_string(s):
    return s[::-1]
print(reverse_string("Hello"))
print()

# task 5
"""  Написати функцію, яка приймає список слів та повертає найдовше слово у списку.
"""
print("task5")
def longest_word(words):
    return max(words, key=len)
print(longest_word(["hello", "cat", "word", "Python"]))
print()

# task 6
"""  Написати функцію, яка приймає два рядки та повертає індекс першого входження другого рядка
у перший рядок, якщо другий рядок є підрядком першого рядка, та -1, якщо другий рядок
не є підрядком першого рядка."""
print("task6")
def find_substring(str1, str2):
        len1, len2 = len(str1), len(str2)
        for i in range(len1 - len2 + 1):
            if str1[i:i + len2] == str2:
                return i
        return -1

str1 = "Hello, world!"
str2 = "world"
print(find_substring(str1, str2)) # поверне 7

str1 = "The quick brown fox jumps over the lazy dog"
str2 = "cat"
print(find_substring(str1, str2)) # поверне -1
print()

# task 7
# task 8
# task 9
# task 10
"""  Оберіть будь-які 4 таски з попередніх домашніх робіт та
перетворіть їх у 4 функції, що отримують значення та повертають результат.
Обов'язково документуйте функції та дайте зрозумілі імена змінним.
"""

print("task7")
# task 03 з домашки 4
""" Зробіть так, щоб у тексті було не більше одного пробілу між словами.
"""
import re

def normalize_spaces(text: str) -> str:
    """
    Прибирає зайві пробіли між словами, залишаючи лише один.
    """
    return re.sub(r' +', ' ', text)

print(normalize_spaces("Привіт, як    справи?"))
print(normalize_spaces("один   два три     чотири"))
print()

print("task8")
# task 05 з домашки 4
""" Виведіть, скільки слів у тексті починається з Великої літери?
"""
def count_capitalized_words(text: str) -> int:
    """
    Повертає кількість слів у тексті, які починаються з великої літери.
    """
    words = text.split()
    count = 0

    for word in words:
        if word[0].isupper():
            count += 1

    return count

text = "Привіт, як справи? Мене звати Максим."
print(count_capitalized_words(text))
print()

print("task9")
# task 06 з домашки 4
""" Виведіть позицію, на якій слово Tom (кіт) зустрічається вдруге
"""
def second_occurrence_position(text: str, word: str) -> int:
    """
    Повертає позицію (індекс у списку слів), на якій задане слово
    зустрічається вдруге. Якщо слово зустрічається менше двох разів,
    повертає -1.
    """
    words = text.split()
    count = 0

    for i, w in enumerate(words):
        if w == word:
            count += 1
            if count == 2:
                return i

    return -1

text = "кіт сидить на вікні, а інший кіт спить на дивані"
print(second_occurrence_position(text, "кіт"))
print()

print("task10")
# task 10 з домашки 4
""" Виведіть кількість слів останнього речення (з adventures_of_tom_sawer_sentences).
"""
import re


def last_sentence_word_count(text: str) -> int:
    """
    Повертає кількість слів в останньому реченні тексту.
    """
    # Розбиваємо текст на речення за крапкою, знаком оклику чи питання
    sentences = re.split(r'[.!?]+', text)

    # Прибираємо порожні елементи
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0

    last_sentence = sentences[-1]
    words = last_sentence.split()

    return len(words)

text = "Привіт, як справи? Мене звати Максим."
print(last_sentence_word_count(text))