from typing import Dict, List


class Interval:
    def __init__(self, t1: int, t2: int) -> None:
        self.start = t1
        self.finish = t2

    def intersect(self, other) -> bool:
        if (
            ((self.finish > other.start) and (other.start >= self.start))
            or (
                (other.finish > self.start)
                and (
                    (other.finish <= self.finish)
                    or (other.finish > self.finish)
                    and self.finish > other.start
                )
            )
            or ((self.start == other.start) and (self.finish == other.finish))
        ):
            return True
        else:
            return False

    def calculate_intersection(self, other) -> int:
        if self.intersect(other):
            # Один интервал полностью "в другом"
            if ((self.start >= other.start) and (self.finish <= other.finish)) or (
                (other.start >= self.start) and (other.finish <= self.finish)
            ):
                return min(self.finish - self.start, other.finish - other.start)
            # self-интервал "слева", other уходит "вправо"
            elif (self.start <= other.start) and (self.finish > other.start):
                return self.finish - other.start
            # other "слева", self "справа"
            elif (self.start > other.start) and (self.start < other.finish):
                return other.finish - self.start

    def __str__(self) -> str:
        return f"Interval {self.start} - {self.finish}"


def normalize(intervals: List[int]) -> List[int]:
    """Соединяет пересекающиеся отрезки"""

    intervals_copy = intervals.copy()

    for outer_interval_index in range(0, len(intervals_copy) - 1, 2):
        outer_interval = Interval(
            intervals_copy[outer_interval_index],
            intervals_copy[outer_interval_index + 1],
        )

        for inner_interval_index in range(0, len(intervals_copy) - 1, 2):
            inner_interval = Interval(
                intervals[inner_interval_index], intervals[inner_interval_index + 1]
            )

            # Проверяем, что внутренний и внешний интервалы - не одинаковые и пересекаются
            # Если условия выполняются - удаляем входы и выходы обоих интервалов и вносим в список объединенный интервал.
            if (
                outer_interval_index != inner_interval_index
            ) and outer_interval.intersect(inner_interval):

                # Определяем индексы элементов интервалов, подлежащих объединению
                remove_indexes = [
                    outer_interval_index,
                    outer_interval_index + 1,
                    inner_interval_index,
                    inner_interval_index + 1,
                ]
                jnt_interval_start = min(
                    outer_interval.start, inner_interval.start
                )  # Объединенный интервал имеет минимальное время старта
                jnt_interval_finish = max(
                    outer_interval.finish, inner_interval.finish
                )  # и максимальное время финиша

                # Через включение списков собираем новый список интервалов, не включая в него элементы объединенных интервалов
                # и добавляя один объединенный интервал
                return normalize(
                    [
                        i
                        for j, i in enumerate(intervals_copy)
                        if j not in remove_indexes
                    ]  # не включаем элементы объединенных интервалов
                    + [jnt_interval_start]  # включаем старт объединенного интервала
                    + [jnt_interval_finish]  # включаем финиш объединенного интервала
                )

    return sorted(intervals_copy)  # Сортировать не обязательно


def sort_intervals(intervals: List[int]) -> List[int]:
    """Сортирует входы и выходы участника урока, располагая в правильном временном порядке."""
    sorted_intervals = []
    intervals_entries = [i for index, i in enumerate(intervals) if index % 2 == 0]
    intervals_exits = [i for index, i in enumerate(intervals) if index % 2 != 0]
    for i in range(len(intervals_entries)):
        sorted_intervals.append(sorted(intervals_entries)[i])
        sorted_intervals.append(sorted(intervals_exits)[i])

    return sorted_intervals


def correct_interval_for_lesson(interval: Interval, lesson: Interval):
    """Двигает начало/конец интервала, если тот за пределами рамок урока.
    Повторялось в коде, решил вынести в отдельную функцию.
    """
    if interval.start < lesson.start:
        interval.start = lesson.start
    if interval.finish > lesson.finish:
        interval.finish = lesson.finish


def appearance(intervals: Dict[str, List[int]]) -> int:
    """Основная функция скрипта"""
    lesson = Interval(intervals["lesson"][0], intervals["lesson"][1])

    time = 0

    # Приводим в порядок оба списка интервалов. Объединяем пересекающиеся и сортируем интервалы.
    pupils = normalize(sort_intervals(intervals["pupil"]))
    tutors = normalize(sort_intervals(intervals["tutor"]))

    # Внешним циклом пройдем по интервалам ученика
    for i in pupils[::2]:
        pupil = Interval(i, pupils[pupils.index(i) + 1])

        # Интервалы за пределами урока не считаем
        if pupil.intersect(lesson):

            # Если ученик зашел раньше, начался урок, или вышел позже, чем урок окончился, меняем ему время.
            correct_interval_for_lesson(pupil, lesson)

            # Внутренним циклом - по отрезкам учителя
            for j in tutors[::2]:
                tutor = Interval(j, tutors[tutors.index(j) + 1])
                if tutor.intersect(lesson):

                    correct_interval_for_lesson(tutor, lesson)

                    # Считаем время, если интервалы пересекаются
                    if pupil.intersect(tutor):

                        time += pupil.calculate_intersection(tutor)

    return time


tests = [
    {
        "data": {
            "lesson": [1594663200, 1594666800],
            "pupil": [
                1594663340,
                1594663389,
                1594663390,
                1594663395,
                1594663396,
                1594666472,
            ],
            "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
        },
        "answer": 3117,
    },
    {
        "data": {
            "lesson": [1594702800, 1594706400],
            "pupil": [
                1594702789,
                1594704500,
                1594702807,
                1594704542,
                1594704512,
                1594704513,
                1594704564,
                1594705150,
                1594704581,
                1594704582,
                1594704734,
                1594705009,
                1594705095,
                1594705096,
                1594705106,
                1594706480,
                1594705158,
                1594705773,
                1594705849,
                1594706480,
                1594706500,
                1594706875,
                1594706502,
                1594706503,
                1594706524,
                1594706524,
                1594706579,
                1594706641,
            ],
            "tutor": [
                1594700035,
                1594700364,
                1594702749,
                1594705148,
                1594705149,
                1594706463,
            ],
        },
        "answer": 3577,
    },
    {
        "data": {
            "lesson": [1594692000, 1594695600],
            "pupil": [1594692033, 1594696347],
            "tutor": [1594692017, 1594692066, 1594692068, 1594696341],
        },
        "answer": 3565,
    },
]

if __name__ == "__main__":
    for i, test in enumerate(tests):
        test_answer = appearance(test["data"])
        assert (
            test_answer == test["answer"]
        ), f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
