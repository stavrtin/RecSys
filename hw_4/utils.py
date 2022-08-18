import pandas as pd
import numpy as np


def prefilter_items(data, take_n_popular=5000, item_features=None):
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
 
    # Уберем самые популярные товары (их и так купят)
    top_popular = popularity[popularity['share_unique_users'] > 0.2].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]

    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.02].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]

    # Уберем товары, которые не продавались за последние 12 месяцев
    data = data[data['week_no'] < 12 * 4]
    
    # Уберем не интересные для рекоммендаций категории (department)
    

    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.

    # Уберем слишком дорогие товары
    
    # Возбмем топ по популярности
    popularity = data.groupby('item_id')['quantity'].sum().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)

    top_5000 = popularity.sort_values('n_sold', ascending=False).head(take_n_popular).item_id.tolist()
        
    # Заведем фиктивный item_id (если юзер не покупал товары из топ-5000, то он "купил" такой товар)
    data.loc[~data['item_id'].isin(top_5000), 'item_id'] = 999999

    
    # ...

    return data


def postfilter_items(user_id, recommednations):
    pass