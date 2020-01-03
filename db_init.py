import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
create_user_table = "CREATE TABLE IF NOT EXISTS users (" \
               "    id INTEGER PRIMARY KEY, " \
               "    username text, " \
               "    password text" \
               ")"
create_item_table = "CREATE TABLE IF NOT EXISTS items (" \
                    "   itemId INTEGER PRIMARY KEY," \
                    "   name text," \
                    "   price real" \
                    ")"

cursor.execute(create_user_table)
cursor.execute(create_item_table)


admin = (1, 'admin', 'easy')
users = [(2, 'bob', 'bob2'),
         (3, 'anne', 'xyz')
         ]
items = [(1, 'flower', 9.99)]

insert_query = "INSERT INTO users VALUES (?, ?, ?)"

cursor.execute(insert_query, admin)
cursor.executemany(insert_query, users)

insert_query = "INSERT INTO items VALUES (?, ?, ?)"
cursor.executemany(insert_query, items)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

select_query = "SELECT * FROM items"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()

def get_cursor():
    return cursor