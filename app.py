from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/calorie_tracker/nutrition.db'
db = SQLAlchemy(app)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    foods = Food.query.all()
    total = {
        'calories': sum(f.calories for f in foods),
        'protein': sum(f.protein for f in foods),
        'fat': sum(f.fat for f in foods),
        'carbs': sum(f.carbs for f in foods)
    }
    return render_template('index.html', foods=foods, total=total)


@app.route('/add', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        food = Food(
            name=request.form['name'],
            calories=float(request.form['calories']),
            protein=float(request.form['protein']),
            fat=float(request.form['fat']),
            carbs=float(request.form['carbs'])
        )
        db.session.add(food)
        db.session.commit()
        return redirect('/')
    return render_template('add_food.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
