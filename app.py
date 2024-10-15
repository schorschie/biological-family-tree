from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Config for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///family.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Family model
class Family(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(100), nullable=False)
  last_name = db.Column(db.String(100), nullable=False)
  date_of_birth = db.Column(db.String(20), nullable=False)
  place_of_birth = db.Column(db.String(100), nullable=False)
  mother_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=True)
  father_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=True)
  gender = db.Column(db.String(1), nullable=False)


# Route to the homepage to display records
@app.route('/')
def index():
  records = Family.query.all()
  return render_template('index.html', records=records)

# Route to add a new person
@app.route('/add', methods=['GET', 'POST'])
def add_person():
  if request.method == 'POST':
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    place_of_birth = request.form['place_of_birth']
    mother_id = request.form['mother_id'] or None
    father_id = request.form['father_id'] or None
    gender = request.form['gender']

    # Validate gender
    if gender not in ['m', 'w', 'd']:
      return "Invalid gender value", 400

    new_person = Family(
      first_name=first_name,
      last_name=last_name,
      date_of_birth=date_of_birth,
      place_of_birth=place_of_birth,
      mother_id=mother_id,
      father_id=father_id,
      gender=gender
    )
    db.session.add(new_person)
    db.session.commit()
    return redirect(url_for('index'))

  return render_template('add_person.html')

if __name__ == '__main__':
  app.run(debug=__debug__)
