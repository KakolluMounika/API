from flask import Flask,redirect,url_for,request,render_template
from flask_cors import CORS, cross_origin
from flask import jsonify, make_response
import mysql.connector
import requests
app = Flask(__name__,static_url_path='/static')

CORS(app)
mydb = mysql.connector.connect(
		host="localhost",
		user = "root",
		passwd = "Mouni$444",
		database = "passwords"
		)
mycursor = mydb.cursor()
#app.add_url_rule('/', 'hello', 'hello_world') TEMPLATES
#app.config['CORS_HEADERS'] = 'application/json'
@app.route('/')
def start():
	return render_template("index.html")

@app.route('/login',methods=['POST'])
def login():
	
	#passwd = str(passwd)[3:-3]
	#result = str(result)[3:-3]
	if(request.method=='POST'):
		idno =  request.form['idno']
		pswd =  request.form['pswd']
		tu = (idno,)
		sql = "select password from students where idno=%s"
		mycursor.execute(sql,tu)
		passwd = mycursor.fetchone()
		if(str(passwd)!="None"):
			if(passwd[0]==pswd):
				output = {'msg' : 'success', 'data' : {
					'idno' : idno,
					'name' : pswd,
 				}}
				return make_response(jsonify(output), 200)
			else:
				output = {'msg' : 'failed', 'error' : 'invalid details'}
				return make_response(jsonify(output), 404)
		else:
			output = {'msg' : 'failed', 'error' : 'user does not exist'}
			return make_response(jsonify(output),404)

# This is used for signup page
@app.route('/signup',methods=['GET','POST'])
def Sign_Up():
	return render_template("signup.html")
@app.route('/registration',methods=['POST'])
def Registration():
	if(request.method=='POST'):
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		idno = request.form['idno']
		email = request.form['email']
		passwd = request.form['pswd']
		sql = "select idno from students where idno=%s"
		mycursor.execute(sql,(idno,))
		idn = mycursor.fetchone() 
		if(str(idn)=='None'):
			tu = (idno,firstname,lastname,email,passwd)
			sql = "insert into students (idno,firstname,lastname,email,password) values(%s,%s,%s,%s,%s)"
			mycursor.execute(sql,tu)
			mydb.commit()
			output = {'msg' : 'success','data' : 'sign up successful'}
			return make_response(jsonify(output),200)
		else:
			output = {'msg' : 'failed','error' : 'user already exist'}
			return make_response(jsonify(output),404)

# Change Password
@app.route('/changepasswd',methods=['GET','POST'])
def cp():
	return render_template("change-password.html")
@app.route('/changepassword',methods=['GET','POST'])
def ChangePassword():
	if(request.method == 'POST'):
		idno = request.form['idno']
		oldpass = request.form['oldpassword']
		newpass = request.form['newpassword']
		sql = "select password from students where idno=%s and password=%s"
		tu = (idno,oldpass)
		mycursor.execute(sql,tu)
		paswd = mycursor.fetchone()
		if(paswd=='None'):
			output = {'msg' : 'failed','error':'invalid details'}
			return make_response(jsonify(output),404)
		else:
			sql = "update students set password=%s where idno=%s"
			tu = (newpass,idno);
			mycursor.execute(sql,tu);
			mydb.commit()
			output = {'msg': 'success','data':'password is changed successful'}
			return make_response(jsonify(output),200)
			
if __name__ == '__main__':
   app.run(threaded=True,debug=True)


# open terminal