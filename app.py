from flask import *
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="projectx",
    password="")

@app.route('/')
@app.route('/home')
def home():
    cursor = mydb.cursor()
    cursor.execute("select * from martabak")
    data = cursor.fetchall()
    return render_template('home.html',data=data) 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    cursor = mydb.cursor()
    jenis = request.form["jenis"]
    isian = request.form["isian"]
    harga = request.form["harga"]
    query = ("insert into martabak values( %s, %s, %s, %s)")
    data = ( "", jenis, isian, harga )
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return redirect("/home")

@app.route('/aksi_login', methods =["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("select * from user where username = %s and password = %s")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    if value:
        session["user"] = username
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    if session.get("user"):
        cursor = mydb.cursor()
        cursor.execute("select * from martabak")
        data = cursor.fetchall()
        return render_template('admin.html',data=data) 
    else:
        return redirect(url_for("login"))
    

@app.route('/hapus/<id_martabak>')
def hapus(id_martabak):
    cursor = mydb.cursor()
    query = ("delete from martabak where id_martabak = %s")
    data = (id_martabak,)
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return redirect('/admin')

@app.route('/update/<id_martabak>')
def update(id_martabak):
    cursor = mydb.cursor()
    query = ("select * from martabak where id_martabak = %s")
    data = (id_martabak,)
    cursor.execute( query, data )
    value = cursor.fetchone()
    return render_template('update.html',value=value) 

@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    cursor = mydb.cursor()
    id_martabak = request.form["id_martabak"]
    jenis = request.form["jenis"]
    isian = request.form["isian"]
    harga = request.form["harga"]
    query = ("update martabak set jenis = %s, isian = %s, harga = %s where id_martabak = %s")
    data = ( jenis, isian, harga,id_martabak, )
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True)