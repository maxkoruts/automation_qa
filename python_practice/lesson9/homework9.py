class Rhombus:
    def __init__(self, side_a: float, angle_a: float):
        self.сторона_а = side_a
        self.кут_а = angle_a

    def __setattr__(self, name, value):
        if name == "сторона_а":
            if value <= 0:
                raise ValueError("Сторона повинна бути більше 0")
            super().__setattr__(name, value)

        elif name == "кут_а":
            if not (0 < value < 180):
                raise ValueError("Кут повинен бути в діапазоні від 0 до 180 градусів")
            super().__setattr__(name, value)
            # Автоматично обчислюємо суміжний кут
            super().__setattr__("кут_б", 180 - value)

        else:
            super().__setattr__(name, value)

    def __str__(self):
        return (f"Ромб:\n"
                f"  Сторона a: {self.сторона_а}\n"
                f"  Кут a: {self.кут_а}°\n"
                f"  Кут b: {self.кут_б}°")

#використання
rhombus = Rhombus(side_a=6, angle_a=45)
print(rhombus)