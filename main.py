import requests
import re
import html
import math

url = "https://porsche.ua/model/911"

response = requests.get(url)
response_text = response.text

response_text = html.unescape(response_text)
response_text = re.sub(r"<[^>]+>", " ", response_text)
response_text = " ".join(response_text.split())

start = response_text.find("Моделі та характеристики")
response_text = response_text[start:]

models = [
    "911 Carrera",
    "911 Carrera T",
    "911 Carrera S Coupe",
    "911 Carrera 4S",
    "911 Carrera GTS",
    "911 Carrera 4 GTS"
]

expense_groups = [
    (15000, {"Їжа": 40, "Житло та комунальні": 25, "Одяг": 5, "Транспорт": 10, "Інше": 10}),
    (30000, {"Їжа": 30, "Житло та комунальні": 20, "Одяг": 6, "Транспорт": 8, "Інше": 10}),
    (60000, {"Їжа": 22, "Житло та комунальні": 15, "Одяг": 6, "Транспорт": 7, "Інше": 10}),
    (float("inf"), {"Їжа": 15, "Житло та комунальні": 10, "Одяг": 5, "Транспорт": 6, "Інше": 9}),
]


def get_expenses(salary):
    for limit, percents in expense_groups:
        if salary <= limit:
            return {name: salary * p / 100 for name, p in percents.items()}


cars = []

print("СПИСОК АВТОМОБІЛІВ PORSCHE 911\n")

for model in models:
    index = response_text.find(model)

    if index != -1:
        text_part = response_text[index:index + 150]

        price = re.search(r"від\s*([\d\s]+)\s*грн", text_part)

        if price:
            price_uah = int(price.group(1).replace(" ", ""))

            cars.append([model, price_uah])

            print(len(cars), model)
            print("Ціна:", format(price_uah, ",").replace(",", " "), "грн")
            print()

choice = int(input("Виберіть автомобіль за номером: "))

if choice < 1 or choice > len(cars):
    print("Неправильний номер!")
else:
    car_name = cars[choice - 1][0]
    car_price = cars[choice - 1][1]

    print("\nВи вибрали:", car_name)

    salary = float(input("Введіть зарплату за місяць (грн): "))

    expenses_dict = get_expenses(salary)
    expenses = sum(expenses_dict.values())
    savings = salary - expenses

    print("\nВИТРАТИ НА МІСЯЦЬ")
    for name, value in expenses_dict.items():
        print(name + ":", round(value), "грн")
    print("Усього витрат:", round(expenses), "грн")

    if savings <= 0:
        print("Ви не можете відкладати гроші!")
    else:
        months = math.ceil(car_price / savings)
        years = months // 12
        remaining_months = months % 12

        print("\nРЕЗУЛЬТАТ")
        print("Автомобіль:", car_name)
        print("Вартість:", format(car_price, ",").replace(",", " "), "грн")
        print("Зарплата:", salary, "грн")
        print("Заощадження за місяць:", round(savings), "грн")

        print("Потрібно працювати:", months, "місяців")
        print("Або:", years, "років і", remaining_months, "місяців")