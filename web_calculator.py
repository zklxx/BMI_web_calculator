from flask import Flask, render_template, request, url_for, flash, redirect
import mysql.connector
import time
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

#TODO 
#SQL injection protection
#Data validation, divide by 0

mydb = mysql.connector.connect(
  host="mysql",
  user="root",
  password="0306",
  database="ibiza"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES LIKE 'bmi'") 
test_schema = mycursor.fetchall()
print(test_schema)
if not test_schema:
    mycursor.execute("CREATE TABLE bmi (name VARCHAR(255), age INT, weight INT, height FLOAT, bmi_score FLOAT, date DATETIME)")


app = Flask(__name__, static_url_path='/files', static_folder="files")
app.config['SECRET_KEY'] = '5705ba21b160ad17e59949db821541703dc565c813755fca'


@app.route('/')
def index():
    sql = "SELECT * FROM bmi ORDER BY date DESC"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    records = mycursor.fetchall()
    data = map(lambda a: (a[0], int(a[1]), int(a[2]), float(a[3]), float(a[4]), time.strptime(a[5], '%Y-%m-%d %H:%M:%S')), records)  
    df = pd.DataFrame(records, columns=("name", "age", "weight", "height", "bmi_score", "date")) 
    plot = sns.relplot(x="bmi_score", y="age", data=df, kind="scatter")
    plot_fig = plot.fig
    plot_fig.savefig("files/scatterplot.png")
    return render_template('index.html', messages=records, image_path="/files/scatterplot.png") #named argument

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        mycursor = mydb.cursor()
        name = request.form['name']
        age = request.form["age"]
        weight = request.form['weight']
        height = request.form['height']
        sql = "INSERT INTO bmi (name, age, weight, height, bmi_score, date) VALUES (%s, %s, %s, %s, %s, %s)"
        if not name:
            flash('Name is required!')
        elif not age:
            flash('Age is required!')
        elif not weight:
            flash('Weight is required!')
        elif not height:
            flash('Height is required!')
        else:
            val = (name, age, weight, height, calculate_bmi(int(weight), float(height))["BMI"], time.strftime('%Y-%m-%d %H:%M:%S'))
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/about/')
def about():
    return render_template('about.html')

def calculate_bmi(weight, height):
    return weight/height**2    



