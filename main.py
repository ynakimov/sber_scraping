import database as db
import sber_scrap as sber

def sql_bulk_insert_without_check(data):
    records = []
    len_price = len(data['dates'])
    i = 0
    while (i < len_price):
        # Готовим список кортежей для массовой вставки
        records.append((data['dates'][i], data['prices_sell'][i], data['prices_buy'][i]))
        i += 1  
    db.sql_bulk_insert_without_check(db.get_connection(), records)


def main():
    db.create_table(db.get_connection())
    current_date = db.get_maximum_date(db.get_connection())
    price_gold = sber.get_data_to_dictionary_for_period(current_date, 'PMR-4', 'A98', structure='for_plotly')
    sql_bulk_insert_without_check(price_gold)
    price_data = db.get_all_data(db.get_connection())
    sber.show_diagram(price_data)
    



if __name__ == '__main__':
    main()