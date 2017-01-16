import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

import urllib.error


def do_parsing(min_idx, max_idx):

    sources = []
    labels = []

    for i in range(min_idx, max_idx):
        # url текущей страницы
        url = "http://ideone.com/recent/" + str(i)

        # скачиваем страницу и создаём из неё объект soup
        data = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(data, "lxml")

        for block in soup.find_all('div', class_='source-view'):
            spans = block.find_all('span')

            # язык
            language = spans[0].text
            # отметка об успешности компиляции
            valid_mark = spans[3].text

            if valid_mark == 'Success':
                # часть ссылки на страницу с кодом
                link = block.find('strong').text

                # файл с кодом находится по адресу http://ideone.com/plain/{переменная link}
                # скачиваем его
                response = urllib.request.urlopen('http://ideone.com/plain/' + link[1:])
                data = response.read() 
                text = data.decode('utf-8')

                # если кол-во строк в коде меньше 50, то добавляем 
                # текущий исходный код и метку языка в соответствующие списки
                if text.count('\n') < 50:
                    sources.append(text)
                    labels.append(language)
                    
    return (sources, labels)


def write_to_new_dataframe(sources, labels):
    df = pd.DataFrame({'source': sources, 'language': labels})
    df.to_csv('data/raw_data.csv', index=False)


def append_to_dataframe(sources, labels):
    df1 = pd.read_csv('raw_data.csv')
    df2 = pd.DataFrame({'source': sources, 'language': labels})
    
    # объединяем датафреймы
    new_df = pd.concat([df1, df2])
    
    # убираем дублирующиеся строки
    new_df.drop_duplicates(inplace=True)
    
    new_df.to_csv('raw_data.csv', index=False)


def stable_parse(min_idx, max_idx, step):
	for i in range(min_idx, max_idx, step):
	    try:
	        sources, labels = do_parsing(i, i + step)
	        append_to_dataframe(sources, labels)
	        print('OK!')
	    except urllib.error.HTTPError:
	        print('Error! Continue...')
	        continue