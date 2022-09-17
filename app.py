import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_company(id):
    conn = get_db_connection()
    company = conn.execute('SELECT * FROM company WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if company is None:
        abort(404)
    return company


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    conn = get_db_connection()
    companies = conn.execute('SELECT * FROM company').fetchall()
    conn.close() 
    return render_template('index.html', companies=companies)


@app.route('/<int:company_id>')
def company(company_id):
    company = get_company(company_id)
    return render_template('company.html', company=company)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        industry = request.form['industry']

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO company (name, industry) VALUES (?, ?)',
                         (name, industry))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    company = get_company(id)

    if request.method == 'POST':
        name = request.form['name']
        industry = request.form['industry']

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE company SET name = ?, industry = ?'
                         ' WHERE id = ?',
                         (name, industry, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', company=company)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    company = get_company(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM company WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(company['name']))
    return redirect(url_for('index'))
