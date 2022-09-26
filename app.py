from ast import If
from crypt import methods
from sre_constants import SUCCESS
import flask
from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

#Configuredb
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


app.secret_key = "super secret key"

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        #fetch from data
        empDetails = request.form
        epid = empDetails['eid']
        epassword = empDetails['password']
        cur = mysql.connection.cursor()
        # empid = cur.execute("INSERT INTO Holiday_db.login(e_id, e_password) VALUES(%s, %s)", (epid, epassword))
        empid = cur.execute("SELECT e_id FROM Holiday_db.Employee WHERE e_password = %s AND e_id = %s", (epassword, epid))
        # empid = cur.fetchone()
        if empid == True :
            # self.engine.say('invalid')
            empDetails = cur.fetchall()

            # return render_template('Employee', empid=empid)
            # session['empDetails'] = empid
            return redirect('/portal')
        # else:
        #     self.engine.say('successfull')
        # mysql.connection.commit()
        # cur.close()
        # return redirect('/Employee')
        return 'FAILURE'
    return render_template('index.html')

@app.route('/portal',methods=['GET', 'POST'])
def portal():

    return render_template('portal.html')


@app.route('/Employee',methods=['GET', 'POST'])
def Employee():
    
    # emp = emp.get(empid)
    # emp = request.args['emp']  # counterpart for url_for()
    # emp = session['emp']       # counterpart for session
    # return render_template("foo.html", messages=json.loads(messages))
    cur = mysql.connection.cursor()
    empResult = cur.execute("SELECT e_id, e_name, e_designation FROM Holiday_db.Employee")

    if empResult > 0:
        empDetails = cur.fetchall()
        return render_template('Employee.html', empDetails=empDetails)



@app.route('/signup')
def signup():
    return redirect('/register')
    # return render_template('register.html')



@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #fetch from data
        empReg = request.form
        eid = empReg['eid']
        name = empReg['name']
        designation = empReg['designation']
        password = empReg['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Holiday_db.Employee(e_id, e_name, e_designation, e_password) VALUES(%s, %s, %s, %s)", (eid, name, designation, password))
        mysql.connection.commit()
        cur.close()
        return redirect('/')

    return render_template('register.html')



@app.route('/holiday',methods=['GET','POST'])

def holiday():
    if request.method == 'POST':
        hday1 = request.form
        name=hday1['name']
        date=hday1['date']
        cur = mysql.connection.cursor()
        cur.execute("insert into Holiday_db.Holiday(h_name,h_date) values(%s,%s)",(name,date))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('holiday.html')



@app.route('/holidayList')

def holidayList():
    cur = mysql.connection.cursor()
    hday = cur.execute("SELECT * FROM Holiday_db.Holiday")
    
    if hday > 0:
        hday1 = cur.fetchall()
        return render_template('holiday_list.html', hday1=hday1)





@app.route('/leave',methods=['GET','POST'])
def leave():
    if request.method == 'POST':
        lday = request.form
        eid=lday['eid']
        name=lday['name']
        date=lday['date']
        cur = mysql.connection.cursor()
        cur.execute("insert into Holiday_db.Leave(e_id,l_name,l_date) values(%s,%s,%s)",(eid,name,date))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('leave.html')


@app.route('/leave_list')

def leave_list():
    cur = mysql.connection.cursor()
    lday1 = cur.execute("SELECT * FROM Holiday_db.Leave")
    
    if lday1 > 0:
        lday = cur.fetchall()
        return render_template('leave_list.html', lday=lday)

@app.route('/cal')

def cal():
    return render_template('cal.html')

if __name__ == '__main__':
    app.run(debug=True)