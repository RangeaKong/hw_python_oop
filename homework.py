from typing import Type, List
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.'
               )

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    H_IN_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        message: InfoMessage = InfoMessage(str(self.__class__.__name__),
                                           self.duration,
                                           self.get_distance(),
                                           self.get_mean_speed(),
                                           self.get_spent_calories()
                                           )
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * (self.duration * self.H_IN_M))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    MULTIPLIER: float = 0.035
    SQUARE_AVG: float = 0.029
    KM_IN_MS = round(1000 / 3600, 3)
    M_IN_SM: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных каллорий."""
        duration_minutes = self.duration * self.H_IN_M
        avg_speed_mc = self.get_mean_speed() * self.KM_IN_MS
        heigt_meters = self.height / self.M_IN_SM
        return ((self.MULTIPLIER * self.weight
                 + (avg_speed_mc**2 / heigt_meters)
                 * self.SQUARE_AVG * self.weight) * duration_minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    SWIMMING_SPEED_OFFSET: float = 1.1
    SWIMMING_SPEED_MULTIPLIER: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWIMMING_SPEED_OFFSET)
                * self.SWIMMING_SPEED_MULTIPLIER * self.weight * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    acceptable_types: dict[str, Type[Training]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking
                                                   }
    if workout_type in acceptable_types:
        return acceptable_types[workout_type](*data)
    raise TypeError('Acceptable_types: Incorrect Value.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[tuple[str, list]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [3000, 2.512, 75.8, 180.1]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
