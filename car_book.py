#Користувач (Клієнт) може переглянути список доступних автомобілів.
#Користувач може обрати автомобіль та забронювати його.
#Система повинна реєструвати, який автомобіль був виданий.
#Користувач повинен отримати Підтвердження Прокату (Rental Confirmation) або Договір, який містить деталі оренди.

class Car:
    def __init__(self, model, year, price, is_available=True):
        self.model = model
        self.year = year
        self.price = price
        self.is_available = is_available

    def __str__(self):
        return f"{self.model} ({self.year}) - ${self.price} - {'Доступний' if self.is_available else 'Зарезервований'}"


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

    # добавляем несколько авто
    system.add_car(Car("BMW M1", 2023, 100))
    system.add_car(Car("Mazda 6", 2020, 70))
    system.add_car(Car("Audi A4", 2022, 90))

    # показываем доступные авто
    system.show_available_cars()

    # спрашиваем у пользователя номер машины
    try:
        choice = int(input("Введіть номер авто для бронювання: ")) - 1
        chosen_car = system.choose_car(choice)

        if chosen_car:
            customer_name = input("Введіть ваше ім'я: ")
            days = int(input("На скільки днів ви хочете орендувати авто? "))

            ticket = system.reserve_car(chosen_car, customer_name, days)
            if ticket:
                print("\n Оренда підтверджена!")
                print(ticket)
    except ValueError:
        print("Помилка: потрібно вводити число.")



if __name__ == "__main__":
    main()

