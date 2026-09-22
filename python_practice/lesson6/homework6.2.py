while True:
    word = input("Введіть слово, яке містить літеру 'h': ")
    if "h" in word.lower():
        print(f"Слово '{word}' прийнято.")
        break
    else:
        print(f"У слові '{word}' немає літери 'h'..")