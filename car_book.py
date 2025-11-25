#Користувач (Клієнт) може переглянути список доступних автомобілів.
#Користувач може обрати автомобіль та забронювати його.
#Система повинна реєструвати, який автомобіль був виданий.
#Користувач повинен отримати Підтвердження Прокату (Rental Confirmation) або Договір, який містить деталі оренди.
import pandas as pd

# ------------------- Клас Авто -------------------
class Car:
    def __init__(self, car_id, make, model, year, price, available="yes"):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.is_available = str(available).lower() == "yes"  # True/False

    def __str__(self):
        status = "Доступний" if self.is_available else "Зарезервований"
        return f"[{self.car_id}] {self.make} {self.model} ({self.year}) - {status}"


# ------------------- Клас Плейлистів -------------------
class PlaylistService:
    def __init__(self):
        self.playlists = {
            "Chill/Relax": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO",
            "Energy/Party": "https://open.spotify.com/playlist/37i9dQZF1DXaXB8fQg7xif",
            "Road Trip Classics": "https://open.spotify.com/playlist/37i9dQZF1DX5q67B6Yd6Z3",
            "Hip-Hop": "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
            "Lo-Fi": "https://open.spotify.com/playlist/37i9dQZF1DX2TR4aV3Ee2X",
            "Pop Hits": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
        }

    def get_playlist(self, mood):
        return self.playlists.get(mood, None)


# ------------------- Квиток Оренди -------------------
class CarRentTicket:
    def __init__(self, car, customer_name, days, playlist_name=None, playlist_link=None):
        self.car = car
        self.customer_name = customer_name
        self.days = days
        self.total_price = car.price * days
        self.playlist_name = playlist_name
        self.playlist_link = playlist_link

    def __str__(self):
        base_info = (f"Квиток оренди:\n"
                     f"Клієнт: {self.customer_name}\n"
                     f"Авто: {self.car.make} {self.car.model} ({self.car.year})\n"
                     f"Днів: {self.days}\n"
                     f"Сума: ${self.total_price}")
        if self.playlist_name and self.playlist_link:
            base_info += (f"\n\n🎶 Ідеальний Плейлист:\n"
                          f"Настрій: {self.playlist_name}\n"
                          f"Посилання: {self.playlist_link}")
        return base_info


# ------------------- Система Оренди -------------------
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

    def reserve_car(self, car, customer_name, days, playlist_name=None, playlist_link=None):
        if car and car.is_available:
            car.is_available = False
            ticket = CarRentTicket(car, customer_name, days, playlist_name, playlist_link)
            return ticket
        else:
            print("Авто недоступне для бронювання.")
            return None


# ------------------- Основний цикл -------------------
def main():
    system = CarRentalSystem()
    playlist_service = PlaylistService()

    # 1. Загружаем CSV
    df = pd.read_csv("cars.csv")

    # 2. Создаём объекты Car из строк CSV
    for _, row in df.iterrows():
        car = Car(row["car_id"], row["make"], row["model"], row["year"], row["price"], row["is_available"])
        system.add_car(car)

    while True:
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

                # Опція плейлиста
                add_playlist = input("Бажаєте додати опцію 'Ідеальний Плейлист'? (yes/no): ")
                playlist_name, playlist_link = None, None
                if add_playlist.lower() == "yes":
                    mood = input("Оберіть настрій/жанр (Chill/Relax, Energy/Party, Road Trip Classics, Hip-Hop, Lo-Fi, Pop Hits): ")
                    playlist_link = playlist_service.get_playlist(mood)
                    if playlist_link:
                        playlist_name = mood
                    else:
                        print("На жаль, такого плейлиста немає.")

                ticket = system.reserve_car(chosen_car, customer_name, days, playlist_name, playlist_link)

                if ticket:
                    print("\n Оренда підтверджена!")
                    print(ticket)

                    # 5. Обновляем DataFrame и сохраняем обратно в CSV
                    df.loc[choice, "is_available"] = "no"
                    df.to_csv("cars.csv", index=False)

        except ValueError:
            print("Помилка: потрібно вводити число.")


if __name__ == "__main__":
    main()

