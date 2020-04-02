from flask import make_response, flash, redirect, url_for, session, request, logging
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from flask_wtf import Form
from wtforms import DateField, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import bcrypt
import pdfkit
from twilio.rest import Client
from datetime import date
import dbConnect
import mysql.connector as mysql
import os


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "secret key"

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'webapp'
# init MYSQL
mysql = MySQL(app)

@app.route("/")
def main():
   return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO webapp.login_details (username, password,email) VALUES (%s,%s,%s)",(username,hash_password,email))
        mysql.connection.commit()
        cur.close()
        flash('registered')

        return redirect(url_for('login'))
    return render_template("register.html", form=form)



    #if request.method == 'POST':
        #Get Form Fields
    #    username = request.form['username']
    #    password_candidate= request.form['password']
        #return render_template("login.html")
        # Create cursor
    #    cur = mysql.connection.cursor()
        #Get user by username
    #    result = cur.execute("SELECT * FROM webapp.login_details WHERE username = %s" ,[username])

    #    if result > 0:
        # Get Stored hash
    #        data = cur.fetchone()
    #        password = data['password']

            # Compare Passwords
    #        if sha256_crypt.verify(password_candidate,password):
                #Passed
    #            session['logged_in'] = True
    #            session['username'] = username

    #            flash('You are now logged in ','success')
    #            return redirect(url_for('dashboard'))
    #        else:
    #            error = 'Username not found'
    #            return render_template('login.html',error=error)
                #close connection
    #        cur.close()
    #    else:
    #        error = 'Username not found'
    #        return render_template('login.html',error=error)
    #return render_template('login.html')



@app.route('/dashboard')
def dashboard():
   return render_template("dashboard.html")

class CustomerForm(Form):
    customer_id = StringField('customer_id', [validators.Length(min=0, max=5)])
    firstname = StringField('firstname', [validators.Length(min=0, max=1)])
    lastname = StringField('lastname', [validators.Length(min=0, max=1)])
    email = StringField('email', [validators.Length(min=0, max=5)])
    contact = StringField('contact', [validators.Length(min=2, max=200)])
    address = TextAreaField('address', [validators.Length(min=30)])

@app.route('/addCustomer', methods=['GET', 'POST'])
#@is_logged_in
def addCustomer():
    form = CustomerForm()
    if form.validate_on_submit():
        print("YES")
        idd = form.id.data
        print(idd)
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        contact = form.contact.data
        address= form.address.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO webapp.customer(id, firstname, lastname, email, contact, address) VALUES(%s, %s, %s, %s, %s, %s)", (idd, t, status, capacity, title, description))

        mysql.connection.commit()

        cur.close()

        flash('Facility Added Successfully', 'success')

        return redirect(url_for('addCustomer'))
    print(form.errors)
    return render_template('addCustomer.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']


        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM login_details WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        product_id = request.form['id']
        product_name = request.form['name']
        location = request.form['location']
        quantity = request.form['quantity']
        cost = request.form['cost']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
               UPDATE stock
               SET name=%s, location=%s, quantity=%s, cost=%s
               WHERE id=%s
            """, (product_name, location, quantity,cost,product_id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return 'updated'
        #return redirect(url_for('Index'))
    return render_template('index.html',msg=msg)



if __name__ =='__main__':
    app.run(debug=True)
