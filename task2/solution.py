import csv
import collections
from typing import List, Dict, Tuple, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Константы для удобства
BASE_URL = "https://ru.wikipedia.org"
START_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
OUTPUT_FILENAME = "beasts.csv"

def get_animals_from_page(page_url: str) -> Tuple[List[str], Optional[str]]:
    """
    Получает список животных с одной страницы категории и ссылку на следующую страницу.
    """
    print(f"Обрабатывается страница: {page_url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        # Проверяем, что запрос прошел успешно
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Не удалось загрузить страницу {page_url}: {e}")
        return [], None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем основной блок контента, где находится список
    content_div = soup.find('div', id='mw-pages')
    if not content_div:
        return [], None

    # Извлекаем все элементы списка животных
    animal_list = [li.text for li in content_div.find_all('li')]

    # Ищем ссылку на следующую страницу
    next_page_link = content_div.find('a', string='Следующая страница')
    next_page_url = None
    if next_page_link and 'href' in next_page_link.attrs:
        # Составляем полный URL из базового и относительного
        next_page_url = urljoin(BASE_URL, next_page_link['href'])
        
    return animal_list, next_page_url

def get_all_animals(start_url: str) -> List[str]:
    """
    Собирает названия всех животных со всех страниц пагинации.

    Args:
        start_url: Начальный URL категории.

    Returns:
        Полный список всех названий животных.
    """
    all_animals = []
    current_url: Optional[str] = start_url
    
    while current_url:
        animals_on_page, next_url = get_animals_from_page(current_url)
        all_animals.extend(animals_on_page)
        current_url = next_url
        
    return all_animals

def count_by_first_letter(names: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество названий на каждую букву алфавита.

    Args:
        names: Список названий для подсчета.

    Returns:
        Словарь, где ключ - первая буква, значение - количество.
    """
    # collections.Counter - идеальный инструмент для такой задачи
    counts = collections.Counter()
    for name in names:
        if name: # Пропускаем пустые строки, если они вдруг появятся
            first_letter = name[0].upper()
            counts[first_letter] += 1
    return dict(sorted(counts.items()))

def write_to_csv(counts: Dict[str, int], filename: str):
    """
    Записывает итоговый подсчет в CSV-файл.

    Args:
        counts: Словарь с подсчетами по буквам.
        filename: Имя выходного файла.
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for letter, count in counts.items():
                writer.writerow([letter, count])
        print(f"Результаты успешно записаны в файл {filename}")
    except IOError as e:
        print(f"Ошибка при записи в файл {filename}: {e}")

def main():
    """Основная функция для запуска скрипта."""
    print("Начинается сбор данных с Википедии...")
    all_beasts = get_all_animals(START_URL)
    print(f"Сбор данных завершен. Всего найдено записей: {len(all_beasts)}")
    
    if all_beasts:
        letter_counts = count_by_first_letter(all_beasts)
        write_to_csv(letter_counts, OUTPUT_FILENAME)
    else:
        print("Не найдено ни одного животного. Файл не будет создан.")


if __name__ == '__main__':
    main()