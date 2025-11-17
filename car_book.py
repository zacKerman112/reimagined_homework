#Користувач (Клієнт) може переглянути список доступних автомобілів.
#Користувач може обрати автомобіль та забронювати його.
#Система повинна реєструвати, який автомобіль був виданий.
#Користувач повинен отримати Підтвердження Прокату (Rental Confirmation) або Договір, який містить деталі оренди.
import pandas as pd

class Car:
    def __init__(self, car_id, make, model, year, available="yes"):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.available = available.lower() == "yes"  # преобразуем в True/False

    def __str__(self):
        status = "Доступний" if self.available else "Зарезервований"
        return f"[{self.car_id}] {self.make} {self.model} ({self.year}) - {status}"


class CarRentTicket:
    def __init__(self, car, customer_name, days):
        self.car = car
        self.customer_name = customer_name
        self.days = days
        self.total_price = car.price * days

    def __str__(self):
        return (f"Квиток оренди:\n"
                f"Клієнт: {self.customer_name}\n"
                f"Авто: {self.car.model} ({self.car.year})\n"
                f"Днів: {self.days}\n"
                f"Сума: ${self.total_price}")


class CarRentalSystem:
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def show_available_cars(self):
        print("Доступні автомобілі:")
        for idx, car in enumerate(self.cars, start=1):
            if car.is_available:
                print(f"{idx}. {car}")

    def choose_car(self, index):
        if 0 <= index < len(self.cars):
            car = self.cars[index]
            if car.is_available:
                return car
            else:
                print("Цей автомобіль вже зарезервований.")
        else:
            print("Невірний вибір.")
        return None

    def reserve_car(self, car, customer_name, days):
        if car and car.is_available:
            car.is_available = False
            ticket = CarRentTicket(car, customer_name, days)
            return ticket
        else:
            print("Авто недоступне для бронювання.")
            return None


# ------------------- Основний цикл програми -------------------

def main():
    system = CarRentalSystem()

    # 1. Загружаем CSV
    df = pd.read_csv("cars.csv")

    # 2. Создаём объекты Car из строк CSV
    for _, row in df.iterrows():
        car = Car(row["model"], row["year"], row["price"], row["is_available"])
        system.add_car(car)

    while True:  #  основной цикл, можно бронировать несколько машин
        system.show_available_cars()

        choice = input("Введіть номер авто для бронювання (або 'exit' для виходу): ")
        if choice.lower() == "exit":
            print("Програма завершена.")
            break

        try:
            choice = int(choice) - 1
            chosen_car = system.choose_car(choice)

            if chosen_car:
                customer_name = input("Введіть ваше ім'я: ")
                days = int(input("На скільки днів ви хочете орендувати авто? "))
                ticket = system.reserve_car(chosen_car, customer_name, days)

                if ticket:
                    print("\n Оренда підтверджена!")
                    print(ticket)

                    # 5. Обновляем DataFrame и сохраняем обратно в CSV
                    df.loc[choice, "is_available"] = False
                    df.to_csv("cars.csv", index=False)

        except ValueError:
            print("Помилка: потрібно вводити число.")
if __name__ == "__main__":
    main()

