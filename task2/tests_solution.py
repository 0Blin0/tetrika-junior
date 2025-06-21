import unittest
import csv
import io
from unittest.mock import patch, Mock

# Импортируем функции из нашего основного файла
import solution

class TestAnimalCounter(unittest.TestCase):

    def test_count_by_first_letter(self):
        """Тестирует логику подсчета по первой букве."""
        names = ["Аист", "Акула", "Бобр", "Собака", "сокол"]
        expected = {'А': 2, 'Б': 1, 'С': 2}
        result = solution.count_by_first_letter(names)
        self.assertEqual(result, expected)

    def test_write_to_csv(self):
        """Тестирует корректность записи в CSV."""
        counts = {'А': 10, 'Б': 5}
        # Используем io.StringIO для имитации файла в памяти
        string_io = io.StringIO()
        
        # Временно "подменяем" встроенную функцию open
        with patch('builtins.open', return_value=string_io, create=True):
            solution.write_to_csv(counts, "dummy_filename.csv")
        
        # Получаем то, что было записано в "файл"
        result = string_io.getvalue().strip()
        expected = "А,10\r\nБ,5"
        self.assertEqual(result, expected)

    @patch('solution.requests.get')
    def test_get_animals_from_page(self, mock_get):
        """
        Тестирует парсинг одной страницы.
        Имитирует ответ от сервера с помощью mock-объекта.
        """
        # HTML-контент для имитации страницы с пагинацией
        mock_html_with_next_page = """
        <html><body>
            <div id="mw-pages">
                <a href="/next_page_link">Следующая страница</a>
                <ul>
                    <li>Антилопа</li>
                    <li>Барсук</li>
                </ul>
            </div>
        </body></html>
        """
        
        # Настраиваем mock-объект, чтобы он возвращал наш HTML
        mock_response = Mock()
        mock_response.text = mock_html_with_next_page
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        animals, next_page = solution.get_animals_from_page("http://dummy.url")
        
        self.assertEqual(animals, ["Антилопа", "Барсук"])
        self.assertEqual(next_page, "https://ru.wikipedia.org/next_page_link")

    @patch('solution.requests.get')
    def test_get_animals_from_last_page(self, mock_get):
        """Тестирует парсинг последней страницы (без ссылки "Следующая")."""
        mock_html_last_page = """
        <html><body>
            <div id="mw-pages">
                <a>Предыдущая страница</a>
                <ul><li>Ягуар</li></ul>
            </div>
        </body></html>
        """
        mock_response = Mock()
        mock_response.text = mock_html_last_page
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        animals, next_page = solution.get_animals_from_page("http://dummy.url/last")

        self.assertEqual(animals, ["Ягуар"])
        self.assertIsNone(next_page) # Ожидаем, что следующей страницы нет

if __name__ == '__main__':
    unittest.main()