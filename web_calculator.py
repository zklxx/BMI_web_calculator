from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '5705ba21b160ad17e59949db821541703dc565c813755fca'

messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        height = request.form['height']

        if not name:
            flash('Name is required!')
        elif not weight:
            flash('Weight is required!')
        else:
            bmi = calculate_bmi(int(weight), float(height))
            messages.append({'name': name, 'content': bmi["comment"] + "%.2f" % bmi["BMI"]})
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
    
