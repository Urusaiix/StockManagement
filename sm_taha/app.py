from flask import Flask, render_template, request, redirect, url_for, flash
from functions import get_db_connection, get_item

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def stock():
    conn = get_db_connection()
    stock = conn.execute('SELECT * FROM stock ORDER BY lokasyon').fetchall()
    conn.close()
    return render_template('stock.html', stock=stock)


@app.route('/<int:id>/edit_stock', methods=('GET', 'POST'))
def edit_stock(id):
    item = get_item(id)
    if request.method == 'POST':
        conn = get_db_connection()
        malzeme = request.form['malzeme']
        malzeme = malzeme.split()
        if len(malzeme) < 4:
            flash('Malzeme is required!')
        else:
            adet = malzeme[1]
            birim = malzeme[2]
            lokasyon = malzeme[3]
            malzeme = malzeme[0]
            conn.execute('UPDATE stock SET malzeme = ?, adet = ?, birim = ?, lokasyon = ?'
                         'WHERE id = ?', (malzeme, adet, birim, lokasyon, id))
        conn.commit()
        conn.close()
        return redirect(url_for('stock'))
    return render_template('edit_stock_adet.html', item=item)


@app.route('/ticket')
def ticket():
    conn = get_db_connection()
    tickets = conn.execute('SELECT * FROM shoppingTicket ORDER BY tarih DESC')
    return render_template('ticket.html', shoppingTicket=tickets)


@app.route('/<int:id>/delete_ticket', methods=('POST',))
def delete_ticket(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM shoppingTicket WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('ticket'))


@app.route('/wish_list', methods=('GET', 'POST'))
def wish_list():
    conn = get_db_connection()
    wish = conn.execute('SELECT * FROM wish_list').fetchall()
    if request.method == 'POST':
        print('methode oke')
        malzeme = request.form['malzeme']
        malzeme = malzeme.split()
        if len(malzeme) < 4:
            flash('Malzeme is required!')
        else:
            adet = malzeme[1]
            birim = malzeme[2]
            lokasyon = malzeme[3]
            malzeme = malzeme[0]
            conn.execute('INSERT INTO wish_list (malzeme, adet, birim, lokasyon) VALUES (?, ?, ?, ?)',
                         (malzeme, adet, birim, lokasyon))
        conn.commit()
        conn.close()
        return redirect(url_for('wish_list'))
    return render_template('wish_list.html', wish_list=wish)


@app.route('/<int:id>/delete_wish', methods=('POST',))
def delete_wish(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM wish_list WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('wish_list'))


@app.route('/<int:id>/delete_item', methods=('POST',))
def delete_item(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM stock WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('stock'))


@app.route('/<int:id>/add_stock', methods=('GET', 'POST'))
def add_stock(id):
    conn = get_db_connection()
    compare = conn.execute(
        'SELECT s.malzeme, s.lokasyon, s.adet, wish_list.malzeme, wish_list.lokasyon, wish_list.adet '
        'FROM wish_list '
        'INNER JOIN stock s  '
        'ON wish_list.malzeme = s.malzeme AND wish_list.lokasyon = s.lokasyon;')
    if compare:
        s_adet = conn.execute('SELECT '
                              's.adet FROM wish_list INNER JOIN stock s '
                              'ON wish_list.malzeme = s.malzeme AND wish_list.lokasyon = s.lokasyon;')
        wl_adet = conn.execute('SELECT '
                               'wish_list.adet FROM wish_list INNER JOIN stock s '
                               'ON wish_list.malzeme = s.malzeme AND wish_list.lokasyon = s.lokasyon;')
        conn.execute('UPDATE stock SET adet = ?', (s_adet + wl_adet,))
    else:
        conn.execute('INSERT INTO stock SELECT * FROM wish_list WHERE id = ?', (id,))
        conn.execute('INSERT INTO shoppingTicket SELECT * FROM wish_list WHERE id = ?', (id,))
        conn.execute('DELETE FROM wish_list WHERE id = ?', (id,))
    conn.commit()
    return redirect(url_for('wish_list'))


if __name__ == '__main__':
    app.run()
