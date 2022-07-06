class Interval:
    def __init__(self, t1, t2) -> None:
        self.start = t1
        self.finish = t2

    def intersect(self, other) -> bool:
        if (
            ((self.finish > other.start) and (other.start >= self.start))
            or ((other.finish > self.start) and ((other.finish <= self.finish) or (other.finish > self.finish) and self.finish > other.start))
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


def appearance(intervals):
    lesson = Interval(intervals['lesson'][0], intervals['lesson'][1]) 
    print("lesson ", lesson)
    time = 0

    # Внешним циклом пройдем по отрезкам ученика
    for i in intervals['pupil'][::2]:
        pupil = Interval(i, intervals['pupil'][intervals['pupil'].index(i)+1])
        print("Pupil ", pupil)

        # Интервалы за пределами урока не считаем

        if pupil.intersect(lesson):
            print("YES")
            # Если ученик зашел раньше, начался урок, или вышел позже, чем урок окончился, меняем ему время.
            if pupil.start < lesson.start:
                pupil.start = lesson.start
            if pupil.finish > lesson.finish:
                pupil.finish = lesson.finish

            # Внутренним циклом - по отрезкам учителя
            for j in intervals['tutor'][::2]:
                tutor = Interval(j, intervals['tutor'][intervals['tutor'].index(j)+1])
                print("Tutor ", tutor)
                if tutor.start < lesson.start:
                    tutor.start = lesson.start
                if tutor.finish > lesson.finish:
                    tutor.finish = lesson.finish
                
                # Считаем время, если интервалы пересекаются
                if pupil.intersect(tutor):
                    print(pupil, tutor, " работаем")
                    time += pupil.calculate_intersection(tutor)
    print("TIME: ", time)
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
