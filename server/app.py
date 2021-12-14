from numpy import nan
from predictor import predict

predictors = [
    {'name': 'Боль в глазу', 'value': False},
    {'name': 'Покраснение', 'value': False},
    {'name': 'Резь в глазах', 'value': False},
    {'name': 'Выделение из глаз - Наличие', 'value': False},
    {'name': 'Выделение из глаз - Характер отделяемого', 'value': False},
    {'name': 'Выделение из глаз - Количество', 'value': False},
    {'name': 'Светобоязнь', 'value': False},
    {'name': 'Слезоточение', 'value': False},
    {'name': 'Неприятные ощущения в глазу', 'value': False},
    {'name': 'Повышенная температура тела', 'value': False},
    {'name': 'Слабость', 'value': False},
    {'name': 'Ощущение инородного тела в глазу', 'value': False},
    {'name': 'Склеивание ресниц утром', 'value': False}
]

iacp_format = {
    'пол': 0,
    'возраст': 0,
    'боль в глазу': 0,
    'покраснение глаза': 0,
    'резь в глазу ': 0,
    'выделение из глаз': 0,
    'выделение из глаза - Характер отделяемого': 0,
    'выделение из глаз - Количество': 0,
    'светобоязнь': 0,
    'слезотечение': 0,
    'неприятные ощущения в глазу': 0,
    'температура тела': 0,
    'слабость': 0,
    'ощущение инородного тела в глазу': 0,
    'склеивание ресниц утром': 0,
    'событие': 0,
    'Unnamed: 16': nan
}


def parameters():
    return predictors


def get_model_value(x):
    return predict(x)


def convert_to_iacp(x):
    for index, predictor in enumerate(iacp_format):
        if index > len(x) - 1:
            break
        iacp_format[predictor] = x[index]
    return iacp_format