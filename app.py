from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

#Conection from bd
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Loreto18'
app.config['MYSQL_DB'] = 'tp-tap'

mysql = MySQL(app)


#Routes

@app.route('/login', methods=['POST','GET'])
def users():
    data = ''
    if(request.method == 'POST'):
        userId = request.form['userid']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userId, password FROM usuario WHERE userid = %s AND password = %s', (userId,password))
        data = cursor.fetchall()
        print('DATA: '+str(data))
    if(data):
        return redirect(url_for('chats')) 
    else:
        return render_template('index.html')

@app.route('/chat')
def chats():
   # if request.method == 'POST':
       # myMessage = request.form['myMessage']
     #   print(myMessage)
       # cursor = mysql.connection.cursor()
        #cursor.execute('INSERT INTO mensaje (mensaje) VALUES (%s)', (myMessage))
        #mysql.connection.commit()
    return render_template('chats.html')

""" def login(): """


@socketio.on('message')
def handleMessage(msg):
    print("Message: " + msg)
    send(msg, broadcast = True)

#Server
if __name__ == '__main__':
    socketio.run(app)
    #app.run(port = 3000, debug = True) #Debug = true is for restart the server automatically

