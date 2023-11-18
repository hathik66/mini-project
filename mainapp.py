# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import re
import yfinance as yf
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)



app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'stockvista'

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)




@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        with mysql.cursor() as cursor:
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                msg = 'Logged in successfully!'
                return render_template('home.html', msg=msg)
            else:
                msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        with mysql.cursor() as cursor:
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {username}_metrics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        stock_id INT,
        Volume FLOAT,
        Open FLOAT,
        High FLOAT,
        Low FLOAT,
        Close FLOAT,
        Drop_8_percent FLOAT,
        Big_sell_off FLOAT,
        Extension_from_base_price FLOAT,
        Price_run_up FLOAT,
        Stock_split FLOAT,
        Good_news FLOAT,
        New_highs FLOAT,
        Distribution FLOAT,
        Full_retracement FLOAT,
        Optimism FLOAT,
        Two_point_gap FLOAT,
        No_rally FLOAT,
        QEPS FLOAT,
        Second_member FLOAT,
        Rumors FLOAT,
        Way_down FLOAT,
        Drop_12_15_percent FLOAT,
        One_day_price_drop FLOAT,
        Poor_rally FLOAT,
        Key_price_support_area FLOAT,
        Up_Down FLOAT,
        Second_confirmation FLOAT,
        Post_analysis FLOAT,
        Support_level FLOAT,
        Week_projection FLOAT,
        Upper_channel_line FLOAT,
        Third_or_fourth_stage_base FLOAT,
        Wide_and_loose FLOAT,
        Moving_average_200_day FLOAT,
        Largest_weekly_volume FLOAT,
        MA_200_day_price_line FLOAT,
        Downtrend FLOAT,
        Poor_relative_strength FLOAT
    )
""")


                cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', (username, password, email,))
                mysql.commit()
                msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

def get_all_stocks():
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # Select all values from the 'stocks' table
            query = "SELECT * FROM stocks"
            cursor.execute(query)

            # Fetch all the rows as a list of dictionaries
            stocks = cursor.fetchall()
    finally:
        connection.close()

    return stocks

# Route to display all stocks
@app.route('/analyze')
def display_stocks():
    stocks = get_all_stocks()
    return render_template('stocks.html', stocks=stocks)

# Create a cursor
    cursor = connection.cursor()    




def add_stock(company_name):
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # Insert a new stock into the 'stocks' table
            query = "INSERT INTO user_stocks (company_name) VALUES (%s)"
            cursor.execute(query, (company_name,))
        connection.commit()
    finally:
        connection.close()
@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock_route():
    if request.method == 'POST':
        # Get the company_name from the form
        company_name = request.form.get('company_name')

        # Add the new stock to the database
        add_stock(company_name)

        # Redirect to the stocks page after adding the stock
        return render_template('home.html')

    return render_template('add_stock.html')




def get_user_stocks():
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # Select all values from the 'stocks' table
            query = "SELECT * FROM user_stocks"
            cursor.execute(query)

            # Fetch all the rows as a list of dictionaries
            stocks = cursor.fetchall()
    finally:
        connection.close()

    return stocks



@app.route('/user_stock')
def display_user_stocks():
    stocks = get_user_stocks()
    return render_template('stocks.html', stocks=stocks)

if __name__ == '__main__':
    app.run(debug=True)


















