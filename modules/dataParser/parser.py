# %%
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import os

# %%
class UserSettings:
    # Инициализация объекта
    def __init__(self, csv_file_path):
        
        self.csv_file_path = csv_file_path  # указываем путь к файлу
        self.name = os.path.basename(csv_file_path).split('.')[0]

        self.df = pd.read_csv(self.csv_file_path, header=None, delimiter=';') # читаем файл
        self.array_2d = self.df.values  #создаем двумерный массив для строк
        self.web_page_url = self.array_2d[1][0] #присваиваем первое значение второй строки как ссылку на веб-страницу

        self.web_element = []
        for i in range(len(self.array_2d[3])):
            self.web_element.append(self.array_2d[2][i])

        self.css_selectors = [] # пустой список селекторов
        for i in range(len(self.array_2d[3])):       # цикл для чтения селекторов первой веб-страницы
            self.css_selectors.append(self.array_2d[3][i])      # заполняем пустой список

        self.tags = []
        for i in range(len(self.array_2d[4])):
            self.tags.append(self.array_2d[4][i])

        self.conditions = []
        for i in range(len(self.array_2d[5])):
            self.conditions.append(self.array_2d[5][i])

        self.titles = [] # пустой список названий столбцов
        for i in range(len(self.array_2d[0])):       # цикл для чтения селекторов первой веб-страницы
            self.titles.append(self.array_2d[0][i]) 
    
    def get_csv_file_path(self):    # получить путь к файлу
        return self.csv_file_path
    
    def get_web_page_url(self):     # получить url страницы
        return self.web_page_url
    
    def get_web_element(self):
        return self.web_element

    def get_css_selectors(self):    # получить селекторы
        return self.css_selectors
    
    def get_tags(self):
        return self.tags
    
    def get_conditions(self):
        return self.conditions

    def get_titles(self):
        return self.titles

    def get_file_name(self):        # получить название файла
        return self.name

# %%
class DataParser:

    def __init__(self, web_page_url, web_element, titles, css_selectors, tags, conditions):
        self.web_page_url = web_page_url
        self.web_element = web_element
        self.titles = titles
        self.css_selectors = css_selectors
        self.tags = tags
        self.conditions = conditions
        print(self.web_element)
    def get_html_content(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        response = requests.get(self.web_page_url, headers=headers)
        if response.status_code == 200:
            self.html_content = response.content
            return print('Successful')      # информирование пользователя о статусе чтения
        else:
            return print(response.status_code)
    
    def extract_data(self):
        #data = {'Title': [], 'Year': [], 'Duration': [], 'Age': []}
        data = {name: [] for name in self.titles}

        soup = BeautifulSoup(self.html_content, 'html.parser')

        metadata_list = soup.find(f'{self.web_element[0]}', class_=f'{self.web_element[1]}')

        for selector,tag in zip(self.css_selectors, self.tags):
            items = metadata_list.find_all(f'{tag}', class_=selector)
            for item in items:
                for condition, title in zip(self.conditions, self.titles):
                    if eval(condition):
                        data[f'{title}'].append(item.text.strip())

        # Получаем максимальную длину списка среди всех столбцов
        max_length = max(len(data[col]) for col in data)

        # Заполняем отсутствующие значения в более коротких столбцах значением по умолчанию (например, '')
        for col in data:
            data[col] += [''] * (max_length - len(data[col]))
        result = pd.DataFrame(data)
        return result

# %%
filename = input("Enter a file-instruction name: ")     # Вводим название файла с расширение (filename.csv)
user_settings = UserSettings(f"D:\ISproject\dataStorage\{filename}")    # Передача файла в класс пользовательских настроек

folder_path = f"D:\\ISproject\\dataStorage\\{user_settings.get_file_name()}"    # Создание каталога для переданного файла
os.makedirs(folder_path, exist_ok=True)

data_collector = DataParser(user_settings.get_web_page_url(), user_settings.get_web_element(), user_settings.get_titles(), user_settings.get_css_selectors(), user_settings.get_tags(), user_settings.get_conditions())
data_collector.get_html_content()       # Сохранение HTML-контента в переменную html_content
result = data_collector.extract_data()  # Сбор данных

time = datetime.now().strftime("%Y%m%d_%H%M")   # Сохранение полученных данных с указанием времени и этапа выполнения
result.to_csv(f"{folder_path}\\{user_settings.get_file_name()}_{time}_parsed.csv", index=False, sep=';')

# %%
# Код для чтения тегов и классов

#import pandas as pd

# Чтение CSV файла в DataFrame
#df = pd.read_csv('file.csv', sep=';', header=None, names=['tag', 'classes'])

# Итерация по строкам DataFrame
#for index, row in df.iterrows():
    #tag = row['tag']
    #classes = row['classes'].split()  # Разделение классов по пробелу
    #print("Тег:", tag)
    #print("Классы:")
    #for class_name in classes:
        #print(class_name)
    #print()  # Пустая строка для разделения вывода между элементами


