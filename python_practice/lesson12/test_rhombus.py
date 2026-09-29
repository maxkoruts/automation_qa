import pytest

from rhombus import Rhombus


def test_створення_ромба_з_коректними_даними():
    """Атрибути встановлюються, а кут_б обчислюється автоматично."""
    r = Rhombus(side_a=6, angle_a=45)

    assert r.сторона_а == 6
    assert r.кут_а == 45
    assert r.кут_б == 135


@pytest.mark.parametrize("side", [0, -1, -0.5])
def test_некоректна_сторона_викликає_помилку(side):
    """Сторона <= 0 неприпустима."""
    with pytest.raises(ValueError, match="Сторона повинна бути більше 0"):
        Rhombus(side_a=side, angle_a=45)


@pytest.mark.parametrize("angle", [0, 180, -10, 200])
def test_некоректний_кут_викликає_помилку(angle):
    """Кут поза межами (0, 180) неприпустимий, включно з граничними значеннями."""
    with pytest.raises(ValueError, match="Кут повинен бути в діапазоні"):
        Rhombus(side_a=5, angle_a=angle)


def test_зміна_кута_оновлює_суміжний_кут():
    """Після зміни кут_а значення кут_б перераховується."""
    r = Rhombus(side_a=5, angle_a=45)

    r.кут_а = 100

    assert r.кут_а == 100
    assert r.кут_б == 80


def test_str_повертає_очікуваний_текст():
    """Рядкове представлення містить сторону та обидва кути."""
    r = Rhombus(side_a=6, angle_a=45)

    expected = (
        "Ромб:\n"
        "  Сторона a: 6\n"
        "  Кут a: 45°\n"
        "  Кут b: 135°"
    )
    assert str(r) == expected
