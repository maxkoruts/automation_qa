def sum_numbers(s):
    return sum(int(x) for x in s.split(","))


data = ["1,3,3,4", "1,2,3,4,50,77", "qwerty1,2,3"]

for item in data:
    try:
        print(sum_numbers(item))
    except ValueError:
        print("Не можу це зробити!")