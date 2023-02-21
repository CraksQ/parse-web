import requests
from bs4 import BeautifulSoup
import csv


def scrape_page(soup, quotes):
    quote_elements = soup.find_all('div', class_='quote')
    for quote_element in quote_elements:
    #извлечение текста из quote
        text = quote_element.find('span', class_= 'text').text
    #зивлечение автора из quote
        author = quote_element.find('small', class_='author').text
    #извлечение тэгов ссылок свзязаный с qoute
        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')

    #сохранение списка строк тегов в списке

    tags = []
    for tag_element in tag_elements:
        tags.append(tag_element.text)
        quotes.append(
            {
                'text':text,
                'autor':author,
                'tags':' , '.join(tags)#объединение тегов в строку
            }
        )
#URL-адрес главной страницы целевого веб-сайта
base_url= 'https://quotes.toscrape.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
page = requests.get(base_url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')
quotes = []
scrape_page(soup, quotes)
#получение страницы и инициализация soup

#получение HTML элемента "Далее"
next_li_element = soup.find('li', class_='next')
#если есть следующая страница для очистки
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    #получение новой страницы
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    #парсинг новой страницы
    soup = BeautifulSoup(page.text, 'html.parser')

    scrape_page(soup, quotes)
    #логическая очистка...

    #поиск HTML-элемента «Далее →» на новой странице
    next_li_element = soup.find('li', class_='next')

    #логическая очистка
    #чтение файла qoutes.csv и создание его
    #если его нет
csv_file = open('quotes.csv', 'w', encoding='utf-8', newline='')
    #инициализация объекта записи для вставки данных в csv файл
writer = csv.writer(csv_file)
    #запись заголовка в csv файл
writer.writerow(['Text', 'Autor', 'Tags'])

    #запись строк
for qoute in quotes:
    writer.writerow(qoute.values())
    #завершение операции и освобождение ресурсов
csv_file.close()

