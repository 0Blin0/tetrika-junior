import unittest
from solution import appearance

class TestAppearanceFunction(unittest.TestCase):

    def test_provided_cases(self):
        """Проверяет тесты из условия задачи."""
        tests = [
            {'intervals': {'lesson': [1594663200, 1594666800],
                           'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                           'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
             'answer': 3117},
            {'intervals': {'lesson': [1594702800, 1594706400],
                           'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                           'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
             'answer': 3577},
            {'intervals': {'lesson': [1594692000, 1594695600],
                           'pupil': [1594692033, 1594696347],
                           'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
             'answer': 3565},
        ]
        
        for i, test in enumerate(tests):
            with self.subTest(i=i):
                self.assertEqual(appearance(test['intervals']), test['answer'])
    
    def test_simple_overlap(self):
        """Тест простого случая, где все три интервала пересекаются."""
        intervals = {
            'lesson': [0, 100],
            'pupil': [10, 90],
            'tutor': [20, 80]
        }
        # Пересечение [20, 80], длительность 60
        self.assertEqual(appearance(intervals), 60)

    def test_no_overlap(self):
        """Тест, когда пересечения нет."""
        intervals = {
            'lesson': [0, 10],
            'pupil': [20, 30],
            'tutor': [40, 50]
        }
        self.assertEqual(appearance(intervals), 0)

    def test_tutor_no_show(self):
        """Тест, когда один из участников (учитель) отсутствует."""
        intervals = {
            'lesson': [0, 100],
            'pupil': [10, 90],
            'tutor': []
        }
        self.assertEqual(appearance(intervals), 0)

    def test_empty_input(self):
        """Тест на пустой входной словарь."""
        self.assertEqual(appearance({}), 0)
        
    def test_touching_intervals(self):
        """Тест, где интервалы соприкасаются, но не пересекаются."""
        intervals = {
            'lesson': [0, 100],
            'pupil': [10, 20],
            'tutor': [20, 30]
        }
        # Пересечения нет, так как в момент времени 20 один уходит, а другой приходит.
        self.assertEqual(appearance(intervals), 0)

    def test_multiple_intersections(self):
        """Тест с несколькими отдельными пересечениями."""
        intervals = {
            'lesson': [0, 100],
            'pupil': [10, 20, 50, 60],
            'tutor': [15, 55]
        }
        # Первое пересечение: [15, 20] -> 5 секунд
        # Второе пересечение: [50, 55] -> 5 секунд
        # Итого: 10 секунд
        self.assertEqual(appearance(intervals), 10)


if __name__ == '__main__':
    unittest.main()