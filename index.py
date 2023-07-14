from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///employee.db'

db = SQLAlchemy(app)

class Employee(db.Model):
    eid = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String, nullable=False)
    esalary = db.Column(db.Float, default=0)
    email = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"Employee('{self.eid}', '{self.ename}', '{self.esalary}', '{self.email}')"

with app.app_context():
    # db.drop_all()
    db.create_all()

CORS(app)
@app.route('/',methods=['GET','POST'])
def home():
    emp_email = request.args.get('empEmail')
    if request.method == 'POST':
        data = request.get_json()
        emp_name = data['ename']
        emp_salary = data['esalary']
        empl_email = data['email']
        
        user_data = {
            "ename": emp_name,
            "esalary": emp_salary,
            "email": empl_email
        }

        user = Employee(ename=emp_name, esalary=emp_salary, email=empl_email)
        db.session.add(user)
        db.session.commit()
        # print(user)
        return jsonify(user_data), 201
    if request.method == 'GET':
        emp = db.session.execute(db.select(Employee).filter_by(email=emp_email)).scalar_one()
        user_data = {
            "eid": emp.eid,
            "ename": emp.ename,
            "esalary": emp.esalary,
            "email": emp.email
        }
        return jsonify(user_data), 200
    
app.run(debug=True)