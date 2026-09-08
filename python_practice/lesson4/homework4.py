adventures_of_tom_sawer = ("""
Tom gave up the brush with reluctance in his .... face but alacrity
in his heart. And while
the late steamer
"Big Missouri" worked ....
and sweated
in the sun,
the retired artist sat on a barrel in the .... shade close by, dangled his legs,
munched his apple, and planned the slaughter of more innocents.
There was no lack of material;
boys happened along every little while;
they came to jeer, but .... remained to whitewash. ....
By the time Ben was fagged out, Tom had traded the next chance to Billy Fisher for
a kite, in good repair;
and when he played
out, Johnny Miller bought
in for a dead rat and a string to swing it with—and so on, and so on,
hour after hour. And when the middle of the afternoon came, from being a
poor poverty, stricken boy in the .... morning, Tom was literally
rolling in wealth."""
)

##  ПЕРЕЗАПИСУЙТЕ зміст змінної adventures_of_tom_sawer у завданнях 1-3
# task 01 ==
""" Дані у строці adventures_of_tom_sawer розбиті випадковим чином, через помилку.
треба замінити кінець абзацу на пробіл .replace("\n", " ")"""

print(f"task 01")
adventures_of_tom_sawer_fixed = adventures_of_tom_sawer.replace("\n", " ")
print(adventures_of_tom_sawer_fixed)
print()

# task 02 ==
""" Замініть .... на пробіл
"""

print(f"task 02")
adventures_of_tom_sawer_fixed = adventures_of_tom_sawer_fixed.replace("....", " ")
print(adventures_of_tom_sawer_fixed)
print()

# task 03 ==
""" Зробіть так, щоб у тексті було не більше одного пробілу між словами.
"""
print(f"task 03")
adventures_of_tom_sawer_fixed = " ".join(adventures_of_tom_sawer_fixed.split())
print(adventures_of_tom_sawer_fixed)
print()

# task 04
""" Виведіть, скільки разів у тексті зустрічається літера "h"
"""
print(f"task 04")
count_h = adventures_of_tom_sawer_fixed.count("h")
print(count_h)
print()

# task 05
""" Виведіть, скільки слів у тексті починається з Великої літери?
"""
print(f"task 05")
words = adventures_of_tom_sawer_fixed
count_upper = sum(1 for word in words if word[0].isupper())
print(count_upper)
print()

# task 06
""" Виведіть позицію, на якій слово Tom зустрічається вдруге
"""
print(f"task 06")
first_pos = adventures_of_tom_sawer_fixed.find("Tom")
second_pos = adventures_of_tom_sawer_fixed.find("Tom", first_pos + 1)
print(second_pos)
print()

# task 07
""" Розділіть змінну adventures_of_tom_sawer по кінцю речення.
Збережіть результат у змінній adventures_of_tom_sawer_sentences
"""
print(f"task 07")
import re
adventures_of_tom_sawer_sentences = re.split(r'(?<=[.!?])\s+', adventures_of_tom_sawer_fixed)
print(adventures_of_tom_sawer_sentences)
print()

# task 08
""" Виведіть четверте речення з adventures_of_tom_sawer_sentences.
Перетворіть рядок у нижній регістр.
"""
print(f"task 08")
fourth_sentence = adventures_of_tom_sawer_sentences[3].lower()
print(fourth_sentence)
print()


# task 09
""" Перевірте чи починається якесь речення з "By the time".
"""
print(f"task 09")
starts_with = any(sentence.startswith("By the time") for sentence in adventures_of_tom_sawer_sentences)
print(starts_with)
print()

# task 10
""" Виведіть кількість слів останнього речення з adventures_of_tom_sawer_sentences.
"""
print(f"task 10")
last_sentence = adventures_of_tom_sawer_sentences[-1]
word_count = len(last_sentence.split())
print(word_count)
print()