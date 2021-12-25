import database as db
import sber_scrap as sber


def sql_bulk_insert_without_check(data):
    records = []
    len_price = len(data['dates'])
    i = 0
    while (i < len_price):
        # Готовим список кортежей для массовой вставки записей в БД.
        records.append((data['dates'][i], data['prices_sell'][i], data['prices_buy'][i]))
        i += 1  
    db.sql_bulk_insert_without_check(db.get_connection(), records)


def main():
    db.create_table(db.get_connection())
    current_date = db.get_maximum_date(db.get_connection())

    data_for_day = sber.get_data_to_dictionary_for_day(current_date,'PMR-4', 'A98')
    if len(data_for_day) > 0:
        entities = (data_for_day['price_sell'], data_for_day['price_buy'], data_for_day['date'])    
        db.sql_update(db.get_connection(), entities)
    
    current_date = db.add_day(current_date, 1)    
    price_gold = sber.get_data_to_dictionary_for_period(current_date, 'PMR-4', 'A98', structure='for_plotly')
    sql_bulk_insert_without_check(price_gold)
    price_data = db.get_all_data(db.get_connection())
    sber.show_diagram(price_data)



if __name__ == '__main__':
    main()