import inspect
from functools import wraps
import unittest

def strict(func):
    """
    Декоратор, который строго проверяет соответствие типов переданных
    аргументов аннотациям типов в сигнатуре функции.
    """
    sig = inspect.signature(func)
    annotations = func.__annotations__

    @wraps(func)  # Сохраняет метаданные оригинальной функции (имя, докстринг и т.д.)
    def wrapper(*args, **kwargs):
        """
        Внутренняя обертка, выполняющая проверку типов перед вызовом
        оригинальной функции.
        """
        try:
            bound_args = sig.bind(*args, **kwargs)
        except TypeError as e:
            raise TypeError(f"Несоответствие аргументов для {func.__name__}: {e}") from e

        # Итерируемся по связанным аргументам (имя_параметра, значение)
        for param_name, value in bound_args.arguments.items():
            # Проверяем, есть ли для данного параметра аннотация типа
            if param_name in annotations:
                expected_type = annotations[param_name]
                actual_type = type(value)

                if actual_type is not expected_type:
                    raise TypeError(
                        f"Аргумент '{param_name}' для функции '{func.__name__}' имеет неверный тип. "
                        f"Ожидал {expected_type.__name__}, но получил {actual_type.__name__}."
                    )
        
        # Если все проверки прошли успешно, вызываем оригинальную функцию
        return func(*args, **kwargs)

    return wrapper

# Пример использования из задания
@strict
def sum_two(a: int, b: int) -> int:
    return a + b

@strict
def build_greeting(name: str, age: int, is_student: bool) -> str:
    status = "student" if is_student else "not a student"
    return f"Привет, {name}! Вам {age} лет, и у вас {status}."


print("--- Примеры работы декоратора ---")
# Корректный вызов
try:
    result = sum_two(1, 2)
    print(f"Сумма двух(1, 2) => {result}")
except TypeError as e:
    print(f"Сумма двух(1, 2) => {e}")

# Некорректный вызов
try:
    sum_two(1, 2.4)
except TypeError as e:
    print(f"Сумма двух(1, 2.4) => {e}")

# Тесты с использованием unittest

class TestStrictDecorator(unittest.TestCase):
    """Набор тестов для декоратора @strict."""

    def test_correct_positional_args(self):
        """Тест: корректные позиционные аргументы проходят проверку."""
        @strict
        def my_func(a: int, b: str):
            return f"{b}{a}"
        # Не должно вызывать исключение
        self.assertEqual(my_func(10, "value"), "value10")

    def test_correct_keyword_args(self):
        """Тест: корректные именованные аргументы проходят проверку."""
        @strict
        def my_func(a: int, b: str):
            return f"{b}{a}"
        # Не должно вызывать исключение
        self.assertEqual(my_func(b="value", a=10), "value10")

    def test_correct_mixed_args(self):
        """Тест: корректные смешанные аргументы проходят проверку."""
        @strict
        def my_func(a: int, b: str, c: float):
            return True
        # Не должно вызывать исключение
        self.assertTrue(my_func(1, "test", c=3.14))

    def test_incorrect_arg_type_raises_type_error(self):
        """Тест: некорректный тип аргумента вызывает TypeError."""
        @strict
        def my_func(a: int, b: str):
            pass
        
        # self.assertRaises — это контекстный менеджер для проверки исключений
        with self.assertRaises(TypeError):
            my_func(1, 2)  # b должен быть str, а не int
            
    def test_error_message_is_descriptive(self):
        """Тест: сообщение об ошибке содержит полезную информацию."""
        @strict
        def my_func(user_id: int):
            pass

        with self.assertRaisesRegex(TypeError, "Аргумент 'user_id'.*Ожидал int.*получил str"):
            my_func(user_id="123")
            
    def test_strictness_int_vs_float(self):
        """Тест: float не принимается на место int."""
        @strict
        def my_func(a: int):
            pass
        with self.assertRaises(TypeError):
            my_func(1.0)
            
    def test_strictness_int_vs_bool(self):
        """Тест: bool не принимается на место int, несмотря на наследование."""
        @strict
        def my_func(a: int):
            pass
        with self.assertRaises(TypeError):
            my_func(True)

    def test_strictness_bool_vs_int(self):
        """Тест: int не принимается на место bool."""
        @strict
        def my_func(a: bool):
            pass
        with self.assertRaises(TypeError):
            my_func(1)
        # Корректный вызов
        self.assertIsNone(my_func(True))


# Блок для запуска тестов при выполнении файла
if __name__ == '__main__':
    print("\n--- Запуск тестов ---")
    unittest.main()