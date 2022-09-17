import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import pandas as pd
import json
import plotly
import plotly.express as px

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    #conn.row_factory = dict_factory
    return conn

def get_company(id):
    conn = get_db_connection()
    company = conn.execute('SELECT * FROM company WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if company is None:
        abort(404)
    return company

def get_cosumptions(company_id):
    conn = get_db_connection()
    consumptions = conn.execute('SELECT * FROM consumptions WHERE company_id = ?',
                        (company_id,)).fetchall()
    conn.close()
    if company is None:
        abort(404)
    return consumptions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    companies = conn.execute('SELECT * FROM company').fetchall()
    df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
      'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
   })
    fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    d = []
    for company in companies:
        consumptions = get_cosumptions(company['id'])
        d.append({"company":company, "consumptions":consumptions})
    conn.close() 
    return render_template('index.html', d=d, graphJSON=graphJSON)

@app.route('/<int:company_id>')
def company(company_id):
    company = get_company(company_id)
    consumptions = get_cosumptions(company_id)
    #print(consumptions)
    return render_template('company.html', company=company, consumptions=consumptions)

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
