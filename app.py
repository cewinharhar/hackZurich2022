from flask import Flask, render_template, request, url_for, flash, redirect, Markup
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.offline as pyo
from company import Company
from db import get_db_connection, get_company, get_consumptions 
import plotly.graph_objects as go
from utils import *

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
        print(c.name, c)
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
        d.append({"company":company, "consumptions":consumptions, 'chart_id':cid})
    conn.close() 
    return render_template('index.html', d=d, graphsJSON=graphsJSON)

@app.route('/<int:company_id>')
def company(company_id):
    company = get_company(company_id)
    #print(company)
    c = Company(company['name'], company['id'], company['industry'], company['summary'])
    consumptions = c.data
    print(c)
    for yearlydata in consumptions:
        #print(yearlydata)
        for year in yearlydata:
            if(year == '2022'):
                months = []
                electricity = []
                for monthlydata in yearlydata[year]:
                    #print(monthlydata)
                    months.append(monthlydata['month'])
                    electricity.append(monthlydata['electricity'])
    df = pd.DataFrame({
            'Electricity Consumption': electricity,
            'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        })
    elecBarPlot = px.bar(df, x='Months', y='Electricity Consumption', title="Monthly Energy consumption in MegaJoule (MJ)", range_y =[800,1400])

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
    company = get_company(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM company WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(company['name']))
    return redirect(url_for('index'))
