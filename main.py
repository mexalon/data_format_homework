import xml.etree.ElementTree as ET
import os
import json


# новости из json
def news_list_from_json(the_path):
    with open(the_path, 'r', encoding='utf-8') as f:  # у меня в винде какие то проблемы с кодировкой по умолчанию
        all_data = json.load(f)

    list_of_news = tuple(item['description'] for item in all_data['rss']['channel']['items'])
    return list_of_news


# новости из XML
def news_list_from_xml(the_path):
    my_parser = ET.XMLParser(encoding='utf-8')  # кодировка по умолчанию, парсер можно не указывать
    tree = ET.parse(the_path, my_parser)
    root = tree.getroot()
    i_fined_it_all = root.findall('channel/item/description')
    list_of_news = tuple(news.text for news in i_fined_it_all)
    return list_of_news


# вычисление топ 10
def get_top_from_list(news_lis):
    all_news = ' '.join(news_lis).split(' ')
    all_words = set(all_news)
    top_ten = sorted([{entry: all_news.count(entry)} for entry in all_words if len(entry) >= 6],
                     key=lambda entry: list(entry.values())[0], reverse=True)[0:10]
    return top_ten


# вывод top 10 слов
def file_processing(file_name):
    the_path = os.getcwd() + '/' + file_name
    if file_name.split('.')[-1] == 'json':
        news_list = news_list_from_json(the_path)
    elif file_name.split('.')[-1] == 'xml':
        news_list = news_list_from_xml(the_path)
    else:
        print('Неверный формат файла')
        news_list = False

    if news_list:
        top_list = get_top_from_list(news_list)
        print(f'Слова, наиболее часто встречающиеся в файе {file_name}: ')
        for entry in top_list:
            print(f'"{list(entry.keys())[0]}" встречается {list(entry.values())[0]} раз')
        print('')


# Задача №1
file_processing('newsafr.xml')

# Задача №2
file_processing('newsafr.json')

