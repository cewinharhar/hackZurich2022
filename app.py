from flask import Flask, render_template, request, url_for, flash, redirect, Markup
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.offline as pyo
from company import Company
from db import *
import plotly.graph_objects as go
from utils import *
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

MONTHS =  ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def my_bar_chart():
    df = pd.DataFrame({
            'Electricity': ['10', '9'],
            'Amount': [4, 1],
            'Months': ['Octomber', 'Semptember']
        })
    fig = px.bar(df, x='Amount', y='Electricity', color='Months', barmode='group', orientation='h')
    my_bar_chart = pyo.plot(fig, output_type='div', include_plotlyjs=False)
    return Markup(my_bar_chart)

@app.route('/')
def index():
    conn = get_db_connection()
    companies = conn.execute('SELECT * FROM company').fetchall()
    d = []
    graphsJSON = []
    for company in companies:
        c = Company(company['name'], company['id'], company['industry'], company['summary'])
        print(c.name, c.score)
        prev_month, prev_value, curr_month, cur_value = get_values(c.data, '2022', 9)
        df = {
            'Electricity': [prev_value, cur_value],
            'Months': [MONTHS[prev_month-1], MONTHS[curr_month-1]]
        }
        fig = px.bar(df, x='Electricity', y='Months', orientation='h')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        cid = 'chart_'+str(company['id'])
        graphsJSON.append({'id': cid, 'df':df, 'graphJSON': graphJSON})
        consumptions = get_consumptions(company['id'])
        d.append({"company":c, "consumptions":consumptions, 'chart_id':cid})
        d.sort(key=lambda x: x['company'].score, reverse=False)
    conn.close() 
    return render_template('index.html', d=d, graphsJSON=graphsJSON)

@app.route('/<int:company_id>')
def company(company_id):
    company = get_company(company_id)
    #print(company)
    c = Company(company['name'], company['id'], company['industry'], company['summary'])
    consumptions = c.data
    last_month, last_year = get_last_date()
    print(c)
    for yearlydata in consumptions:
        #print(yearlydata)
        for year in yearlydata:
            if(year == str(last_year)):
                months = []
                electricity = []
                for monthlydata in yearlydata[year]:
                    #print(monthlydata)
                    months.append(monthlydata['month'])
                    electricity.append(monthlydata['electricity'])
    print(months)
    print(electricity)
    df = pd.DataFrame({
            'Electricity Consumption': electricity,
            'Months': MONTHS[:last_month],
        })
    elecBarPlot = px.bar(df, x='Months', y='Electricity Consumption', title="Monthly Energy consumption in MegaJoule (MJ) in "+str(last_year), range_y =[800,1400])

    fig3 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 270,
        number = { 'suffix': "%" },
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Speed"}))
    #print(df)
    
    elecBarJSON = json.dumps(elecBarPlot, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    #print(c)
    return render_template('company.html', company=company, consumptions=consumptions, elecBarJSON=elecBarJSON, graphJSON3=graphJSON3)

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
    company = get_consumptions(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM company WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(company['name']))
    return redirect(url_for('index'))

@app.route('/delete/month', methods=('GET',))
def delete_months(year=2022, month=12):
    conn = get_db_connection()
    last_year = conn.execute('SELECT DISTINCT year FROM consumptions ORDER BY year DESC').fetchone()
    last_month = conn.execute('SELECT DISTINCT month FROM consumptions where year = ? ORDER BY month DESC', (last_year['year'],)).fetchone()
    new_month = last_month['month']+1
    new_year = last_year['year']
    r = conn.execute('DELETE FROM consumptions WHERE year = ? AND month = ?', (year, month,))
    print(r)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/add', methods=('GET',))
def add_months():
    connection = get_db_connection()
    last_year = connection.execute('SELECT DISTINCT year FROM consumptions ORDER BY year DESC').fetchone()
    last_month = connection.execute('SELECT DISTINCT month FROM consumptions where year = ? ORDER BY month DESC', (last_year['year'],)).fetchone()
    new_month = last_month['month']+1
    new_year = last_year['year']
    if new_month > 12:
        new_month = 1
        new_year += 1
    for company_id in range(11):
        electricity = round(1000 + round(np.random.random(), 2)*150 * np.random.choice([-1, 1, 1, 1]), 1)
        water = round(5 + round(np.random.random(), 2)*150 * np.random.choice([-1, 1, 1, 1]), 1)
        co2 = round(3 + round(np.random.random(), 2)*150 * np.random.choice([-1, 1, 1, 1]), 1)
        r = connection.execute("INSERT INTO consumptions (company_id, year, month, electricity, water, co2) VALUES (?, ?, ?, ?, ?, ?)",
                (company_id, new_year, new_month, electricity, water, co2))
        print(r)
        connection.commit()
    connection.close()
    return redirect(url_for('index'))