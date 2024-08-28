import random
import matplotlib.pyplot as plt

HORIZONTAL = 0
VERTICAL = 1

HUMAN_VELOCITY = 1.3  # m/s
STREET_LENGTH = 100  # m
STREET_WIDTH = 9  # m

TRAFFIC_LIGHTS_ALTERNATION_TIME = 60  # s

NUMBER_OF_EXPERIMENTS = 10000

CITY_MAX_SIZE = 10


class TrafficLight:
    def __init__(self):
        self.initial_green_direction = random.choice([HORIZONTAL, VERTICAL])
        self.initial_time = random.random() * TRAFFIC_LIGHTS_ALTERNATION_TIME

    def _is_initial_green(self, current_time: float) -> bool:
        return (
            current_time - self.initial_time // TRAFFIC_LIGHTS_ALTERNATION_TIME
        ) % 2 == 0

    def is_green(self, current_time: float, direction: int) -> bool:
        # XNOR
        return self._is_initial_green(current_time) == (
            direction == self.initial_green_direction
        )

    def time_to_change(self, current_time: float) -> float:
        return TRAFFIC_LIGHTS_ALTERNATION_TIME - (
            (current_time + self.initial_time) % TRAFFIC_LIGHTS_ALTERNATION_TIME
        )

    def which_direction_is_green(self, current_time: float) -> int:
        return (
            self.initial_green_direction
            if self._is_initial_green(current_time)
            else 1 - self.initial_green_direction
        )

    def is_enougth_time_to_cross(self, current_time: float) -> bool:
        return self.time_to_change(current_time) > time_to_cross_street()


def time_to_cross_street() -> float:
    return STREET_WIDTH / HUMAN_VELOCITY


def time_to_walk_street() -> float:
    return STREET_LENGTH / HUMAN_VELOCITY


def int_to_direction(direction: int) -> str:
    return "horizontal" if direction == HORIZONTAL else "vertical"


def trip_crossings(s: int, e: int) -> int:
    return (e - s) // 2 + (e - s) % 2


def trip_streets(s: int, e: int) -> int:
    return (e - s) - trip_crossings(s, e)


def can_walk_street(coordiate: int) -> bool:
    return coordiate % 2 == 1


def can_cross_street(coordiate: int) -> bool:
    return coordiate % 2 == 0


def traffic_ligth_from_position(position: tuple, traffic_ligths: list) -> TrafficLight:
    return traffic_ligths[position[0] // 2][position[1] // 2]


def main():

    total_times = [0] * CITY_MAX_SIZE
    total_waiting_times = [0] * CITY_MAX_SIZE

    for i in range(CITY_MAX_SIZE):

        CITY_SIZE = i + 1

        CITY_HORIZONTAL_STREETS = CITY_SIZE
        CITY_VERTICAL_STREETS = CITY_SIZE

        START_POINT = (0, 0)
        END_POINT = (CITY_HORIZONTAL_STREETS * 2 - 1, CITY_VERTICAL_STREETS * 2 - 1)

        total_time = 0
        total_waiting_time = 0

        for _ in range(NUMBER_OF_EXPERIMENTS):

            current_time = 0
            current_position = START_POINT

            remaining_horizontal_streets = trip_streets(START_POINT[0], END_POINT[0])
            remaining_vertical_streets = trip_streets(START_POINT[1], END_POINT[1])

            remaining_streets = [
                remaining_horizontal_streets,
                remaining_vertical_streets,
            ]

            remaining_horizontal_crossings = trip_crossings(
                START_POINT[0], END_POINT[0]
            )
            remaining_vertical_crossings = trip_crossings(START_POINT[1], END_POINT[1])

            remaining_crossings = [
                remaining_horizontal_crossings,
                remaining_vertical_crossings,
            ]

            traffic_ligths = [
                [TrafficLight() for _ in range(CITY_HORIZONTAL_STREETS + 1)]
                for _ in range(CITY_VERTICAL_STREETS + 1)
            ]

            while current_position != END_POINT:
                if can_walk_street(current_position[0]) and remaining_streets[0] > 0:
                    current_time += time_to_walk_street()
                    current_position = (current_position[0] + 1, current_position[1])
                    remaining_streets[0] -= 1
                    continue

                if can_walk_street(current_position[1]) and remaining_streets[1] > 0:
                    current_time += time_to_walk_street()
                    current_position = (current_position[0], current_position[1] + 1)
                    remaining_streets[1] -= 1
                    continue

                traffic_light = traffic_ligth_from_position(
                    current_position, traffic_ligths
                )

                if not traffic_light.is_enougth_time_to_cross(current_time):
                    current_time += traffic_light.time_to_change(current_time)
                    total_waiting_time += traffic_light.time_to_change(current_time)

                green_direction = traffic_light.which_direction_is_green(current_time)

                if (
                    can_cross_street(current_position[green_direction])
                    and remaining_crossings[green_direction] > 0
                ):
                    current_time += time_to_cross_street()
                    current_position = (
                        current_position[0] + (green_direction == HORIZONTAL),
                        current_position[1] + (green_direction == VERTICAL),
                    )
                    remaining_crossings[green_direction] -= 1
                    continue

                current_time += traffic_light.time_to_change(current_time)
                total_waiting_time += traffic_light.time_to_change(current_time)
                green_direction = 1 - green_direction

                current_time += time_to_cross_street()
                current_position = (
                    current_position[0] + (green_direction == HORIZONTAL),
                    current_position[1] + (green_direction == VERTICAL),
                )
                remaining_crossings[green_direction] -= 1

            total_time += current_time
            # print("Time:", current_time)

        total_times[i] = total_time / NUMBER_OF_EXPERIMENTS / 60
        total_waiting_times[i] = total_waiting_time / NUMBER_OF_EXPERIMENTS / 60

    # plot times in same graph

    plt.plot(range(1, CITY_MAX_SIZE + 1), total_times, label="Total time")
    plt.plot(range(1, CITY_MAX_SIZE + 1), total_waiting_times, label="Waiting time")
    plt.xlabel("City size")
    plt.ylabel("Time (minutes)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
