import sqlite3
import os
import datetime

DATABASE = 'database\database.db'


def get_connection():
    connection = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    return connection


def check_db(filename):
    return os.path.exists(filename)


def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS price_gold ( 
        date DATE NOT NULL primary key,
        price_sell REAL,
        price_buy REAL
    );"""
    connection.execute(query)
    connection.commit()


def find_by_date(connection, date):
    cursor = connection.cursor()
    values = (date,)
    cursor.execute('select * from price_gold where date = ?', values)
    row = cursor.fetchone()
    if row == None:
        return False
    else:
        return True


def sql_insert(connection, entities, date):
    if find_by_date(connection, date) == False:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO price_gold(date, price_sell, price_buy) VALUES(?, ?, ?)', entities)
        connection.commit()
        connection.close()


def sql_insert_without_check(connection, entities):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO price_gold(date, price_sell, price_buy) VALUES(?, ?, ?)', entities)
    connection.commit()
    connection.close()


def sql_bulk_insert_without_check(connection, entities):
    """ Вставляет большой набор данных """

    if len(entities) == 0:
        connection.close()
        return

    cursor = connection.cursor()
    cursor.executemany('INSERT INTO price_gold(date, price_sell, price_buy) VALUES(?, ?, ?)', entities)
    connection.commit()
    connection.close()


def get_maximum_date(connection):
    """ Получает  макисмальную дату из таблицы """
    cursor = connection.cursor()
    # query = 'SELECT MAX(P.date) AS date FROM price_gold AS P;'
    # Почему-то происходит преобразование типа datetime.date() в тип str() если в запросе применять MAX() 
    query = 'SELECT P.date AS date FROM price_gold AS P ORDER BY date DESC'    
    # data = cursor.execute(query)
    cursor.execute(query)
    row = cursor.fetchone()
    
    if row == None:
        result = datetime.date(2021, 6, 21)
    else:
        result = row[0] + datetime.timedelta(1) #  дельту добавим к дате последних полученных данных                 
    connection.close()
    return result


def get_all_data(connection):
    """ Получает все строки из таблицы """
    dates = []
    prices_sell = []
    prices_buy = []
    cursor = connection.cursor()    
    data = cursor.execute('''SELECT 
                                date AS date, 
                                price_sell AS price_sell, 
                                price_buy AS price_buy 
                            FROM price_gold 
                            ORDER BY date;''')
    for row in data:
        dates.append(row[0])
        prices_sell.append(row[1])
        prices_buy.append(row[2])
     
    price_by_date = {'dates': dates, 'prices_sell': prices_sell, 'prices_buy': prices_buy}
    connection.close()       
    return price_by_date

 
# create_table(connection)
# date = datetime.date(2020, 2, 6)
# entities = (datetime.date(2020, 2, 6), 85.51)
# sql_insert(connection, entities)

# date_2 = datetime.datetime(2021, 6, 21)
# entities = (date_2, 111.51)
# sql_insert(connection, entities)

# find_by_date(connection, date_2)

# connection.close()