from flask import Flask, render_template, g, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('food_data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g,'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()


@app.route('/',methods = ['GET','POST'])
def index():
    db = get_db()

    if request.method == 'POST':
        date = request.form['date']
        dt = datetime.strptime(date,'%Y-%m-%d')
        database_date = datetime.strftime(dt,'%Y%m%d')
        db.execute('insert into date (entry_date) values (?)',[database_date])
        db.commit()
    
    cur = db.execute('select entry_date from date order by entry_date desc')
    results = cur.fetchall()
    r1 = []

    for i in results:
        sd = {}
        d = datetime.strptime(str(i['entry_date']),'%Y%m%d')
        sd['entry_date'] = datetime.strftime(d,'%B %d, %Y')
        r1.append(sd)

    return render_template('home.html',results = r1)


@app.route('/view/<date>',methods = ['GET','POST'])
def view(date):

    db = get_db()
    cur = db.execute('select id,entry_date from date where entry_date = ?',[date])
    date_result = cur.fetchone()

    if request.method == 'POST':
       db.execute('insert into food_date (food_id,log_date_id) values (?,?)',[request.form['food-select'],date_result['id']])
       db.commit()

    d = datetime.strptime(str(date_result['entry_date']),'%Y%m%d')
    ans = datetime.strftime(d,'%B %d, %Y')
    food_items = db.execute('select id,name from food')
    food_results = food_items.fetchall()

    log_cur = db.execute('select food.name, food.protein, food.carbohydrates, food.fat, food.calories \
        from date join food_date on food_date.log_date_id = date.id join food on \
            food.id = food_date.food_id where date.entry_date = ?',[date])

    log_results = log_cur.fetchall()

    prr = 0
    crr = 0
    frr = 0
    cll = 0

    for i in log_results:
        prr += int(i['protein'])
        crr += int(i['carbohydrates'])
        frr += int(i['fat'])
        cll += int(i['calories'])

    return render_template('day.html',date = ans,food = food_results,log = log_results,prr = prr,crr = crr,frr = frr,cll = cll)


@app.route('/add_food',methods = ['GET','POST'])
def add_food():

    db = get_db()

    if request.method == 'POST':
        food = request.form['food-name']
        protein = int(request.form['protein'])
        carb = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])
        calories = protein*4 + carb*4 + fat*9

        db.execute('insert into food (name,protein,carbohydrates,fat,calories) values (?,?,?,?,?)',[food,protein,carb,fat,calories])
        db.commit()

    cur = db.execute('select name,protein,carbohydrates,fat,calories from food')
    results = cur.fetchall()
    
    return render_template('add_food.html', results = results)

if __name__ == '__main__':
    app.run(debug = True)