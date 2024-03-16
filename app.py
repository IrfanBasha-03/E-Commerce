from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/course_reservation_system'
db = SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    student_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main.html')
def main():
    return render_template('main.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/coures.html')
def coures():
    return render_template('coures.html')

# Define a function to create tables within the application context
def create_tables():
    with app.app_context():
        db.create_all()

# Call the function to create tables
create_tables()

@app.route('/submit_form_reservation', methods=['POST'])
def submit_form_reservation():
    course_name = request.form['courseName']
    student_name = request.form['studentName']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']

    # Convert date and time strings to Python datetime objects
    date_object = datetime.strptime(date, '%Y-%m-%d').date()
    time_object = datetime.strptime(time, '%H:%M').time()

    # Create a new Reservation object and add it to the database
    new_reservation = Reservation(course_name=course_name, student_name=student_name, email=email, phone=phone, date=date_object, time=time_object)
    db.session.add(new_reservation)
    db.session.commit()

    return "Reservation submitted successfully!"

@app.route('/submit_form_message', methods=['POST'])
def submit_form_message():
    if request.method == 'POST':
        message_content = request.form['message']
        new_message = Message(content=message_content)
        db.session.add(new_message)
        db.session.commit()
        return "Message submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
