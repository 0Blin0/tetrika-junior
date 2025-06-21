from typing import Dict, List

def appearance(intervals: Dict[str, List[int]]) -> int:
    """
    Вычисляет общее время присутствия ученика и учителя на уроке.
    """
    # Преобразование всех интервалов в список событий "старт" и "конец"
    events = []
    
    # Вспомогательная функция для добавления событий из списка интервалов
    def add_events_from_list(timestamps: List[int]):
        # Итерируемся по парам (старт, конец)
        for i in range(0, len(timestamps), 2):
            start_time, end_time = timestamps[i], timestamps[i+1]
            # Игнорируем некорректные или нулевые интервалы
            if start_time < end_time:
                events.append((start_time, 1))  # +1 для события "старт"
                events.append((end_time, -1))   # -1 для события "конец"

    add_events_from_list(intervals.get('lesson', []))
    add_events_from_list(intervals.get('pupil', []))
    add_events_from_list(intervals.get('tutor', []))
    
    # Если событий нет, то и пересечений нет
    if not events:
        return 0

    # Сортировка событий по времени
    events.sort(key=lambda x: (x[0], -x[1]))

    # Сканирование" временной прямой
    total_intersection_time = 0
    active_participants = 0
    last_event_time = events[0][0]

    for time, event_type in events:
        interval_duration = time - last_event_time
        
        if active_participants == 3:
            total_intersection_time += interval_duration
            
        active_participants += event_type
        last_event_time = time
        
    return total_intersection_time


# Блок для проверки и запуска тестов из задания
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       print(f"Test case {i}: expected={test['answer']}, got={test_answer}")
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
   print("All provided test cases passed!")