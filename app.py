from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orderEase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, default=datetime.date.today)

@app.before_first_request
def create_tables():
    db.create_all()
    if not Order.query.first():
        sample_orders = [
            Order(customer_name='Alice', product_name='Laptop', quantity=1),
            Order(customer_name='Bob', product_name='Phone', quantity=2),
            Order(customer_name='Charlie', product_name='Tablet', quantity=3),
            Order(customer_name='Alice', product_name='Mouse', quantity=2)
        ]
        db.session.bulk_save_objects(sample_orders)
        db.session.commit()

@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)

@app.route('/analytics')
def analytics():
    data = db.session.query(Order.product_name, db.func.sum(Order.quantity)).group_by(Order.product_name).all()
    labels = [d[0] for d in data]
    values = [d[1] for d in data]
    return render_template('analytics.html', labels=labels, values=values)

if __name__ == '__main__':
    app.run(debug=True)
