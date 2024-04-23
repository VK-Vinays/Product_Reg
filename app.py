from flask import Flask, request,render_template, redirect,session, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    prod_discription = db.Column(db.String(500),nullable=False)
    manfacture_info = db.Column(db.String(200), nullable=False)
    serial_number = db.Column(db.String(100), unique=True)
    manfacture_date = db.Column(db.Date, nullable=False)
    warranty_info = db.Column(db.String(100), nullable=True)
    prod_category = db.Column(db.String(100), nullable=True)

    def __init__(self, product_name, prod_discription,
                 manfacture_info, serial_number, manfacture_date,
                 warranty_info, prod_category):
        self.product_name = product_name
        self.prod_discription = prod_discription
        self.manfacture_info = manfacture_info
        self.serial_number = serial_number
        self.manfacture_date = manfacture_date
        self.warranty_info = warranty_info
        self.prod_category = prod_category

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product_reg',methods=['GET','POST'])
def product_reg():
    if request.method == 'POST':
        product_name = request.form['product_name']
        prod_discription = request.form['prod_discription']
        manfacture_info = request.form['manfacture_info']
        serial_number = request.form['serial_number']
        manfacture_date = request.form['manfacture_date']
        warranty_info = request.form['warranty_info']
        prod_category = request.form['prod_category']
        new_product = Product(product_name= product_name,prod_discription= prod_discription,
                           serial_number= serial_number, manfacture_date= convert_date(manfacture_date),
                           manfacture_info= manfacture_info, warranty_info= warranty_info,
                           prod_category= prod_category)
        
        check_product = Product.query.filter_by(product_name=product_name).first()
        check_serialno = Product.query.filter_by(serial_number=serial_number).first()
        if check_product or check_serialno:
            flash("Product already registered with Serial Number {}".format(check_serialno.serial_number))
            return redirect('product_reg')
        db.session.add(new_product)
        db.session.commit()
        flash("Prodcut registered Successfully")
        return redirect('/product_reg')
    return render_template('prod_reg.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name=name,email=email,password=password)
        check_user = User.query.filter_by(name=name).first()
        if check_user:
            flash("User already exists, Try to register with different name")
            return redirect('/register')
        db.session.add(new_user)
        db.session.commit()
        flash("User:{} registered successfully".format(name))
        return redirect('/login')
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            session['name'] = user.name
            flash("Login successfull")
            return redirect('/product_reg')
        else:
            flash("Invalid Login credentials")
            return render_template('login.html',error='Invalid user')
    return render_template('login.html')


def convert_date(str):
    date = datetime.strptime(str, '%Y-%m-%d').date()
    return date

@app.route('/product_search', methods=['GET', 'POST'])
def product_search():
    search_field = request.form.get('searchField')
    search_value = request.form.get('searchValue')

    if search_field == 'product_name':
        products_list = Product.query.filter(Product.product_name.ilike(f'%{search_value}%')).all()
    elif search_field == 'manfacture_info':
        products_list = Product.query.filter(Product.manfacture_info.ilike(f'%{search_value}%')).all()
    elif search_field == 'serial_number':
        products_list = Product.query.filter(Product.serial_number.ilike(f'%{search_value}%')).all()
    else:
        products_list = []

    return render_template('product_search.html', products_list=products_list)

@app.route('/logout')
def logout():
    session.pop('name',None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)