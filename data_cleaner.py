import pandas as pd

def code_cleaner(text):
    '''
    Функция принимает на вход строку текста и удаляет из неё
    все цифры, а также символы табуляции, перевода строки и
    лишние пробелы.
    '''
    for d in '1234567890':
        text = text.replace(d, '')

    text = text.replace('\n', ' ').replace('\t', ' ')
    return ' '.join(text.split())


dataset = pd.read_csv('data/raw_data.csv')

dataset['source'] = dataset['source'].astype(str)
dataset['source'] = dataset['source'].apply(code_cleaner)

dataset.to_csv('data/cleaned_data.csv', index=False)
