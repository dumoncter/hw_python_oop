from dataclasses import dataclass, asdict
from typing import Sequence, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}."
    )

    def get_message(self) -> str:
        """Возвращаем расчетное сообщение о тренировках """
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    LEN_STEP: float = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_1: float = 18
    COEFF_2: float = 20

    def get_spent_calories(self) -> float:
        speed_and_coeff = (
            self.COEFF_1 * self.get_mean_speed() - self.COEFF_2
        ) * self.weight
        dur_in_minutes = self.duration * self.MIN_IN_HOUR

        return speed_and_coeff / self.M_IN_KM * dur_in_minutes


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_1: float = 0.035
    COEFF_2: float = 0.029

    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        weight_and_coeff_1 = self.COEFF_1 * self.weight
        weight_and_coeff_2 = self.COEFF_2 * self.weight
        speed_and_weight = (self.get_mean_speed() ** 2) // self.height
        duration_in_minutes = self.duration * self.MIN_IN_HOUR
        # Тут проблемы с колличеством символом строки превышает 79 символов.
        # Прогнал через онлайн генератор PEP8 выдал так.
        return (
            weight_and_coeff_1 + speed_and_weight * weight_and_coeff_2
        ) * duration_in_minutes


class Swimming(Training):
    """Тренировка: плавание."""

    COEFF_1: float = 1.1
    COEFF_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(
            self, action, duration, weight, length_pool, count_pool
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Расчитать расстояние в бассейне."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Расчитать среднюю скорость в бассейне."""
        distance_in_meters = self.length_pool * self.count_pool
        distance_in_km = distance_in_meters / self.M_IN_KM

        return distance_in_km / self.duration

    def get_spent_calories(self) -> float:
        speed_and_coeff = self.get_mean_speed() + self.COEFF_1

        return speed_and_coeff * self.COEFF_2 * self.weight


def read_package(workout_types: str, data_attr: Sequence[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_name: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    if workout_types not in training_name:
        raise ValueError(
            f'Ошибка. Тренеровка {workout_types} не найдена. '
            f'Проверьте тип тренировки'
        )

    return training_name[workout_types](*data_attr)


def main(main_info) -> None:
    """Главная функция."""

    info = main_info.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
