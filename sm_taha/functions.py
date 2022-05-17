import sqlite3
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_wish(wish_id):
    conn = get_db_connection()
    wish = conn.execute('SELECT * FROM wish_list WHERE id = ?',
                        (wish_id,)).fetchone()

    conn.close()
    if wish is None:
        abort(404)
    return wish


def get_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM stock WHERE id = ?',
                        (item_id,)).fetchone()

    conn.close()
    if item is None:
        abort(404)
    return item
