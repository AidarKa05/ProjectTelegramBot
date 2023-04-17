import sqlite3


def db_add_user(user_id, user_name):
    con = sqlite3.connect('db/database.db')
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO users (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
        con.commit()
    except Exception as error:
        print(error)
    con.close()
