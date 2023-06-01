
import mysql.connector
import csv
from tqdm import tqdm
# TODO: REPLACE THE VALUE OF VARIABLE team (EX. TEAM 1 --> team = 1)
team = 1


# Requirement1: create schema ( name: DMA_team## )
def requirement1(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Creating schema...')
    cursor.execute('drop database if exists DMA_team%02d;' % team)
    cursor.execute('CREATE DATABASE IF NOT EXISTS DMA_team%02d;' % team)

    # TODO: WRITE CODE HERE
    cursor.close()


# Requierement2: create table
def requirement2(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Creating tables...')
    cursor.execute('USE DMA_team%02d;' % team)

    # anime  
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime(
    id INT(11),
    name VARCHAR(255),
    aired VARCHAR(255),
    source VARCHAR(255),
    studio_id INT(11),
    PRIMARY KEY (id) );
    ''')

    # anime_genre
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime_genre(
    anime_id INT(11),
    genre_id INT(11),
    PRIMARY KEY (anime_id, genre_id) );
    ''')

    # anime_licensor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime_licensor(
    anime_id INT(11),
    licensor_id INT(11),
    PRIMARY KEY (anime_id, licensor_id) );
    ''')

    # anime_producer
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime_producer(
    anime_id INT(11),
    producer_id INT(11),
    PRIMARY KEY (anime_id, producer_id) );
    ''')

    # anime_user_rating
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime_user_rating(
    user_id INT(11),
    anime_id INT(11),
    rating INT(11),
    PRIMARY KEY (user_id, anime_id) );
    ''')

    # anime_user_status
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime_user_status(
    user_id INT(11),
    anime_id INT(11),
    watching_status INT(11),
    watching_episodes INT(11),
    PRIMARY KEY (user_id, anime_id) );
    ''')

    # director
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS director(
    producer_id INT(11),
    director VARCHAR(255),
    age INT(11),
    sex VARCHAR(255),
    PRIMARY KEY (producer_id, director) );
    ''')

    # genre
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS genre(
    id INT(11),
    name VARCHAR(255),
    PRIMARY KEY (id) );
    ''')

    # license_sharing
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS license_sharing(
    sharing INT(11),
    shared INT(11),
    sharing_type VARCHAR(255),
    PRIMARY KEY (sharing, shared) );
    ''')

    # licensor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS licensor(
    id INT(11),
    name VARCHAR(255),
    type VARCHAR(255),
    PRIMARY KEY (id) );
    ''')

    # mail
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mail(
    id INT(11),
    user_id INT(11),
    producer_id INT(11),
    body VARCHAR(255),
    PRIMARY KEY (id) );
    ''')

    # producer
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS producer(
    id INT(11),
    name VARCHAR(255),
    PRIMARY KEY (id) );
    ''')

    # studio
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS studio(
    id INT(11),
    name VARCHAR(255),
    nom INT(11),
    genre_id INT(11),
    PRIMARY KEY (id) );
    ''')

    # user
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
    id INT(11),
    name VARCHAR(255),
    PRIMARY KEY (id) );
    ''')

    # TODO: WRITE CODE HERE
    cursor.close()


# Requirement3: insert data
def requirement3(host, user, password, directory):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Inserting data...')
    cursor.execute('USE DMA_team%02d;' % team)


    table_name = ['anime', 'anime_genre', 'anime_licensor', 'anime_producer', 'anime_user_rating','anime_user_status', 
                  'director', 'genre', 'license_sharing', 'licensor', 'mail', 'producer', 'studio', 'user']

    for table in table_name:
        print(table)
        filepath = directory + '/' + table + '.csv'

        f = open(filepath)
        csv_data = csv.reader(f)
        with open(filepath, 'r', encoding = 'cp949') as csv_data:
            next(csv_data, None)  # skip the headers

            if table in ['anime_genre', 'anime_licensor', 'anime_producer', 'genre', 'producer', 'user']:
                for row in  tqdm(csv_data):
                    row = row.strip().split(sep=',')
                    # Change the null data
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s)', row)
                    cnx.commit()

            elif table in ['anime_user_rating', 'license_sharing', 'licensor']:
                for row in  tqdm(csv_data):
                    row = row.strip().split(sep=',')
                    # Change the null data
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp        
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s)', row)
                    cnx.commit()

            elif table in ['anime_user_status','director','studio', 'mail']:
                for row in  tqdm(csv_data):
                    row = row.strip().split(sep=',')
                    # Change the null data
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s,%s)', row)
                    cnx.commit()


            elif table in ['anime']:
                for row in tqdm(csv_data):
                    # Change the null data
                    row = row.strip().split(sep='"')
                    row = row[0].split(',')[0:-1] + [row[1]] + row[2].split(',')[2:]
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s,%s,%s)', row)
                    cnx.commit()

    # TODO: WRITE CODE HERE
    cursor.close()


# Requirement4: add constraint (foreign key)
def requirement4(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Adding constraints...')
    cursor.execute('USE DMA_team%02d;' % team)

    cursor.execute('ALTER TABLE anime ADD CONSTRAINT FOREIGN KEY (studio_id) REFERENCES studio(id);')
    print("constraint 1 added")

    cursor.execute('ALTER TABLE anime_genre ADD CONSTRAINT FOREIGN KEY (anime_id) REFERENCES anime(id);')
    print("constraint 2 added")

    cursor.execute('ALTER TABLE anime_genre ADD CONSTRAINT FOREIGN KEY (genre_id) REFERENCES genre(id);')
    print("constraint 3 added")

    cursor.execute('ALTER TABLE anime_licensor ADD CONSTRAINT FOREIGN KEY (anime_id) REFERENCES anime(id);')
    print("constraint 4 added")

    cursor.execute('ALTER TABLE anime_licensor ADD CONSTRAINT FOREIGN KEY (licensor_id) REFERENCES licensor(id);')
    print("constraint 5 added")

    cursor.execute('ALTER TABLE anime_producer ADD CONSTRAINT FOREIGN KEY (anime_id) REFERENCES anime(id);')
    print("constraint 6 added")

    cursor.execute('ALTER TABLE anime_producer ADD CONSTRAINT FOREIGN KEY (producer_id) REFERENCES producer(id);')
    print("constraint 7 added")

    cursor.execute('ALTER TABLE anime_user_rating ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    print("constraint 8 added")

    cursor.execute('ALTER TABLE anime_user_rating ADD CONSTRAINT FOREIGN KEY (anime_id) REFERENCES anime(id);')
    print("constraint 9 added")

    cursor.execute('ALTER TABLE anime_user_status ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    print("constraint 10 added")

    cursor.execute('ALTER TABLE anime_user_status ADD CONSTRAINT FOREIGN KEY (anime_id) REFERENCES anime(id);')
    print("constraint 11 added")

    cursor.execute('ALTER TABLE license_sharing ADD CONSTRAINT FOREIGN KEY (sharing) REFERENCES licensor(id);')
    print("constraint 12 added")

    cursor.execute('ALTER TABLE license_sharing ADD CONSTRAINT FOREIGN KEY (shared) REFERENCES licensor(id);')
    print("constraint 13 added")

    cursor.execute('ALTER TABLE mail ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    print("constraint 14 added")

    cursor.execute('ALTER TABLE mail ADD CONSTRAINT FOREIGN KEY (producer_id) REFERENCES producer(id);')
    print("constraint 15 added")

    cursor.execute('ALTER TABLE studio ADD CONSTRAINT FOREIGN KEY (genre_id) REFERENCES genre(id);')
    print("constraint 16 added")

    cursor.execute('ALTER TABLE director ADD CONSTRAINT FOREIGN KEY (producer_id) REFERENCES producer(id);')
    print("constraint 17 added")

    # TODO: WRITE CODE HERE
    cursor.close()


# TODO: REPLACE THE VALUES OF FOLLOWING VARIABLES
host = 'localhost'
user = 'root'
password = ''
directory_in = ''

import os

requirement1(host='127.0.0.1', user='root', password='Pk3nAQtcxA@^QLV')
requirement2(host='127.0.0.1', user='root', password='Pk3nAQtcxA@^QLV')

path = os.getcwd()
requirement3(host='127.0.0.1', user='root', password='Pk3nAQtcxA@^QLV', directory=path+'\dataset(project2)')
requirement4(host='127.0.0.1', user='root', password='Pk3nAQtcxA@^QLV')
print('Done!')
