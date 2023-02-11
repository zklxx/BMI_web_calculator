from flask import Flask, render_template, request, url_for, flash, redirect
import mysql.connector
import time

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
    mycursor.execute("CREATE TABLE bmi (name VARCHAR(255), weight INT, height FLOAT, bmi_score FLOAT, date DATETIME)")


app = Flask(__name__)
app.config['SECRET_KEY'] = '5705ba21b160ad17e59949db821541703dc565c813755fca'


@app.route('/')
def index():
    sql = "SELECT * FROM bmi ORDER BY date DESC LIMIT 1"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    records = mycursor.fetchall()
    return render_template('index.html', messages=records) #named argument

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        mycursor = mydb.cursor()
        name = request.form['name']
        weight = request.form['weight']
        height = request.form['height']
        sql = "INSERT INTO bmi (name, weight, height, bmi_score, date) VALUES (%s, %s, %s, %s, %s)"
        if not name:
            flash('Name is required!')
        elif not weight:
            flash('Weight is required!')
        elif not height:
            flash('Height is required!')
        else:
            val = (name, weight, height, calculate_bmi(int(weight), float(height))["BMI"], time.strftime('%Y-%m-%d %H:%M:%S'))
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/about/')
def about():
    return render_template('about.html')

def calculate_bmi(weight, height):
    BMI = weight/height**2
    if BMI > 0:
        if(BMI<16):
            return {"comment":"You have severe thinness: ","BMI":BMI}
        elif(BMI<=16.99):
            return {"comment":"You have moderate thinness: ","BMI":BMI}
        elif(BMI<=18.49):
            return {"comment":"You are underweight: ","BMI":BMI}
        elif(BMI<=24.99):
            return {"comment":"You have normal weight: ","BMI":BMI}
        elif(BMI<=29.99):
            return {"comment":"You are overweight: ","BMI":BMI}
        elif(BMI<=34.99):
            return {"comment":"You are obese: ","BMI":BMI}
        elif(BMI<=39.99):
            return {"comment":"You are severely obese: ","BMI":BMI}
        else:
            return {"comment":"You are morbidly obese: ","BMI":BMI}
    



