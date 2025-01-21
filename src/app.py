#author Lucia Mansogo 

from flask import Flask,render_template,request,redirect,url_for,flash
from dotenv import load_dotenv
from os import getenv
from flask_mysqldb import MySQL
import os



load_dotenv()


app=Flask(__name__)
app.config['MYSQL_HOST']=getenv('MYSQL_HOST')
app.config['MYSQL_USER']=getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD']=getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB']=getenv('MYSQL_DB')
app.secret_key=os.getenv('SECRET_KEY')

mysql=MySQL(app)




@app.route('/')
def index():
    #conexion a la base de datos 
    cur =mysql.connection.cursor()
    cur.execute('Select * from contacts')
    data=cur.fetchall()
    print(data)

    return render_template('index.html',contacts=data)





@app.route('/add_contact',methods=['POST'])
def add_contact():
        #el request es propi del flask 
        if request.method=='POST':
            fullname=request.form['fullname'] #esto  es lo que hay en el name  
            phone=request.form['phone']
            email=request.form['email']

            #REALIZAR LA COEXION A LA BASE DE DATOS
            cur =mysql.connection.cursor()
            cur.execute('insert into contacts(fullname,phone,email) values (%s,%s,%s)',(fullname,phone,email) )
            mysql.connection.commit()

            #el flash lo que hacce es crearno un mensaje pusp pap 
            flash('Contact Added Successfully')
            #Lo que remos decir aqui es que una vez agregado el uusrio que le redirija al metedo que le ruta de del endpoinu raiz de la app
            #el metodo index() que ue esta en la ruta raiz es la que hace esto 
            return redirect(url_for('index'))
            #mysql.connect.close()  
        return 'ADD contact'       #return 'Received'




@app.route('/edit/<string:id>')
def edit_contact(id):

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s',(id,))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])



@app.route('/update/<string:id>', methods=['POST'])
def update_contact(id):

    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname = %s, email = %s, phone = %s WHERE id = %s', (fullname, email, phone, id))

        mysql.connection.commit()
        flash('Contact Updated Successfully')

        return redirect(url_for('index'))
    



@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id=%s',(id,))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('index'))





if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')




