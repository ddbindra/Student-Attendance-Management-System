
from datetime import datetime
from flask import Flask,render_template,url_for,flash,redirect,request,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '6277c7d47f830250e33d86dd45d46651'



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Dhruv'
app.config['MYSQL_PASSWORD'] = 'Dhruv'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)




@app.route("/")
def home():
	return render_template('Attendance.html')





#@app.route("/student")
#def student():
#	return render_template('Student.html')





#@app.route("/teacher")
#def teacher():
#	return render_template('Teacher.html')









@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == "POST":
        details = request.form
        username = details['username']
        email = details['email']
        password = details['pass']
        confirm_password = details['cpass']
        #iid = details['iid']
        cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO register(username, email, password, confirm_password) VALUES (%s, %s, %s, %s)", (username, email, password, confirm_password))
        #cur.execute("INSERT INTO attendance(id, dbms, atc, cn) VALUES (%s, %s, %s, %s)", (iid, dbms, atc, cn))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('register.html')











@app.route("/login_student", methods=['GET','POST'])
def login_student():
	 # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE username = %s AND password = %s', (username, password))
        #cursor.execute('SELECT * FROM attendance WHERE username = %s', (username))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            testies = account['username']
            cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM attendance WHERE username = '{0}'".format(username))
            acc = cur.fetchone()
            # Redirect to home page
            #return 'Logged in successfully!'
            return render_template('display_student.html', account=account, acc=acc)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('login_student.html', msg= msg)

	#form = LoginForm()
	#if form.validate_on_submit():
	#	if form.email.data == 'd@gmail.com' and form.password.data == '123':
	#		flash('You have been logged in!','success')
	#		return redirect(url_for('home'))
	#	else:
	#		flash('Login Unsuccessful. Please check username and password','danger')		
	





@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if request.method == "POST":
        details = request.form
        username = details['username']
        email = details['email']
        password = details['pass']
        confirm_password = details['cpass']
        #iid = details['iid']
        cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO register_teacher(username, email, password, confirm_password) VALUES (%s, %s, %s, %s)", (username, email, password, confirm_password))
        #cur.execute("INSERT INTO attendance(id, dbms, atc, cn) VALUES (%s, %s, %s, %s)", (iid, dbms, atc, cn))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('register.html')






@app.route("/login_teacher", methods=['GET','POST'])
def login_teacher():
	 # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register_teacher WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            #cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            #cursor.execute('SELECT * FROM attendance WHERE id = %s', (account['id']))
            #acc = cursor.fetchone()
            # Redirect to home page
            #return 'Logged in successfully!'
            return render_template('display_teacher.html', account=account)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('login_teacher.html', msg= msg)





@app.route("/display_teacher",methods=['GET','POST'])
def display_teacher():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM register_teacher WHERE id = %s', session['id'])
		#cursor.execute('SELECT * FROM attendance WHERE id = %s', session['id'])
		account = cursor.fetchone()

		"""if request.method == "POST":
			details = request.form
			username = details['username']
			dbms = details['dbms']
			cn = details['cn']
			atc = details['atc']
			cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
			cur.execute("INSERT INTO attendance(username, dbms, cn, atc) VALUES (%s, %s, %s, %s)", (username, dbms, cn, atc))
			mysql.connection.commit()
			cur.close()
			return 'success'"""



		return render_template('display_teacher.html', account=account)
	return redirect(url_for('home'))





@app.route('/display_teacher2', methods=['GET', 'POST'])
def display_teacher2():
    if request.method == "POST":
        details = request.form
        username = details['username']
        dbms = details['dbms']
        cn = details['cn']
        atc = details['atc']
        #iid = details['iid']
        cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO attendance(username, dbms, cn, atc) VALUES (%s, %s, %s, %s)", (username, dbms, cn, atc))
        #cur.execute("INSERT INTO attendance(id, dbms, atc, cn) VALUES (%s, %s, %s, %s)", (iid, dbms, atc, cn))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('display_teacher2.html')







@app.route("/display_student",methods=['GET','POST'])
def display_student():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE id = %s', session['id'])
        account = cursor.fetchone()
        cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM attendance WHERE username = %s',account['username'])
        acc = cur.fetchone()
        return render_template('display_student.html', account=account, acc=acc)
    return redirect(url_for('home'))



@app.route("/display_teacher3",methods=['GET','POST'])
def display_teacher3():
    if request.method == "POST":
        details = request.form
        username = details['username']
        dbms = details['dbms']
        cn = details['cn']
        atc = details['atc']
        cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM attendance')
       
        with open('./outfile.csv','w') as f:
            writer = csv.writer(f)
            for row in cursor.fetchall():
                writer.writerow(row)

        '''print(myresult)
        print(tabulate(myresult, headers=['EmpName', 'EmpSalary'], tablefmt='psql'))'''
        '''for i in range (number_of_rows):
            print (row[i])'''

        #iid = details['iid']
        '''cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO attendance(username, dbms, cn, atc) VALUES (%s, %s, %s, %s)", (username, dbms, cn, atc))
        #cur.execute("INSERT INTO attendance(id, dbms, atc, cn) VALUES (%s, %s, %s, %s)", (iid, dbms, atc, cn))
        mysql.connection.commit()
        cur.close()'''
        return 'success'
    return render_template('display_teacher3.html')


if __name__ == '__main__':
    app.run()