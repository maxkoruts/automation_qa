import csv
from datetime import datetime
from pathlib import Path

import pandas as pd

folder = Path(__file__).parent
file1 = folder / "r-m-c.csv"
file2 = folder / "random-michaels.csv"
out = folder / "result_koruts.csv"


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    return rows[0][:18], rows[1:]


def norm_date(v):
    v = v.strip()
    try:
        return datetime.strptime(v, "%m/%d/%Y").strftime("%m/%d/%Y")
    except ValueError:
        return v


def to_df(rows, cols):
    good = [r[:18] for r in rows if len(r) == 19]  # пропускаємо пошкоджені рядки
    df = pd.DataFrame(good, columns=cols)
    df = df.apply(lambda col: col.str.strip())
    for c in ("Birthday", "EnrolledDate"):
        df[c] = df[c].map(norm_date)
    return df


cols, rows1 = load(file1)
_, rows2 = load(file2)
df1, df2 = to_df(rows1, cols), to_df(rows2, cols)

common = df1.merge(df2, how="inner")
print(f"Спільних рядків між файлами: {len(common)}")

combined = pd.concat([df1, df2], ignore_index=True)
print(f"Рядків до очищення: {len(combined)}")

result = combined.drop_duplicates(keep="first").reset_index(drop=True)
print(f"Рядків після очищення: {len(result)}")

result.to_csv(out, index=False, encoding="utf-8")