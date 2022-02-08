import re

import pandas as pd
import requests
import formatting_explain as Fex
from clickhouse import Clickhouse


def __remove_alphanumeric_token(query):
    query = re.sub('[^\w\d\s]', '', query)
    token_array = query.split(' ')
    regex = r'\b[a-zA-Zа-яА-ЯёЁ]+[0-9]+\w*\b|\b[0-9]+[a-zA-Zа-яА-ЯёЁ]+\w*\b'
    new_query = []
    for token in token_array:
        i = re.search(regex, token)
        if i != '' and i is None:
            new_query.append(token)
    new_query = ' '.join(new_query)
    return new_query


def __remove_alphanumeric_token_2(query):
    query = re.sub('[^\w\d\s]', '', query)
    regex = r'\b[a-zA-Zа-яА-ЯёЁ]+[0-9]+\w*\b|\b[0-9]+[a-zA-Zа-яА-ЯёЁ]+\w*\b'
    new_query = re.sub(regex, '', query)
    return new_query

def __remove_alphanumeric_token_3(query):
    query = re.sub('[^\w\d\s]', '', query)
    token_array = query.split(' ')
    new_query = []
    for token in token_array:
        if len(token) > 2:
            if not (token.isalnum() and not (token.isalpha() or token.isdigit())):
                new_query.append(token)
    new_query = ' '.join(new_query)
    return new_query

def sql_search_queries(date: str) -> str:
    return f"""
        select request, count() as count
        from search.search_log
        where date = '2021-11-25'
        and match(request, '[a-zA-Zа-яА-ЯёЁ]+[0-9]+\w*|\b[0-9]+[a-zA-Zа-яА-ЯёЁ]+\w*\b')
        group by request
        order by count DESC
        limit 2500"""




def clickhouse_get_data():
    SEARCH_DATABASE = 'search'
    CLICKHOUSE_ML_CFG = {'host': '192.168.0.191',
                         'port': '9000',
                         'user': 'devml',
                         'password': 'devml123',
                         'database': SEARCH_DATABASE}

    ml_client = Clickhouse(CLICKHOUSE_ML_CFG)
    sdate = '2021-06-06'
    # edate = '2021-06-16'

    # date_range = pd.date_range(sdate, edate, freq='D').astype(str)
    line_ = f''' '''
    data = ml_client.select(sql_search_queries(sdate))

    with open('search_queries_top_1000.csv', 'w') as file:
        file.write('input,weight')

    for i, j in data.iterrows():
        print(j['count'])
        v2 = re.sub("[^\d\w\s]", " ", j['request'])
        v1 = len(v2.split())
        if v1 > 1:
            with open('search_queries_top_1000.csv', 'a') as file:
                print(j['request'])
                file.write(f'''\n{v2},{j['count']}''')






if __name__ == '__main__':
    # df = clickhouse_get_data()
    # print(df)
    with open('Debug_log_product.txt', 'w') as file:
        file.write(f'Поиск продуктов details \n' '\n\n\n')

    test = []
    # test.append('14')
    # test.append('12')

    # if len(test) > 0:
    #     print(len(test))
    # else:

    # query = '1q q1 11 qq 1q1q1 q1q1q1 feqrfqerf 134534115'

    # new_query = __remove_alphanumeric_token_3(query)


    # print(new_query)

    # query = re.sub('[^\w\d\s]', '', query)
    # token_array = query.split(' ')
    # new_query = []
    # for token in token_array:
    #     print(len(token))
    #     if len(token) > 2:
    #         if not (token.isalnum() and not (token.isalpha() or token.isdigit())):
    #             new_query.append(token)
    # new_query = ' '.join(new_query)


    # print(new_query)
    # query = '1234543143'
    # query2 = '123456789'
    # print(len(query))
    # print(len(query2))
    #
    # difference_size = abs(len(query)-len(query2))
    # if difference_size > 3:
    #     print('true')
    # else:
    #     print('false')




