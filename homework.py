from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    OUTPUT_MESSAGE = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}."
    )

    def get_message(self) -> str:
        return self.OUTPUT_MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f"Метод подсчета каллорий для {type(self).__name__} не определен."
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SEC_IN_MIN = 60
    KMH_IN_MSEC = round(Training.M_IN_KM / (Training.MIN_IN_H * SEC_IN_MIN), 3)

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CM_IN_M = 100
    EXPONENT_2 = 2
    height: float

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (
                    (self.get_mean_speed() * self.KMH_IN_MSEC)
                    ** self.EXPONENT_2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:

        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (
                self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


TRAINING_TYPES: dict = {
    "SWM": Swimming,
    "RUN": Running,
    "WLK": SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TRAINING_TYPES:
        raise ValueError(f"{workout_type} unknown type of training")
    return TRAINING_TYPES[workout_type](*data)


def main(training: Training) -> None:
    print(training.show_training_info().get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
