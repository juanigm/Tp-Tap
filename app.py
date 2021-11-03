from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

#Conection from bd
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ignacio321'
app.config['MYSQL_DB'] = 'tp-tap'

mysql = MySQL(app)


#Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST','GET'])
def login():
    data = ''
    if(request.method == 'POST'):
        userId = request.form['userid']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userId, password FROM usuario WHERE userid = %s AND password = %s', (userId,password))
        data = cursor.fetchall()
        print('DATA: '+str(data))
    if(data):
        return render_template('chats.html')
    else:
        return render_template('index.html')

""" @app.route('/chat', methods=['GET', 'POST'])
def chat():
    print("Hola")
    #if request.method == 'POST':
    #    myMessage = request.form['mensaje']
    #    print(myMessage)
    #    cursor = mysql.connection.cursor()
    #    cursor.execute('INSERT INTO mensaje (mensaje, fecha, idSala, userId) VALUES (%s, %s, %s, %s)', (myMessage, "2/11/21", "Sala123", "Maxi123"))
    #    mysql.connection.commit()
    #
    return redirect """

""" def login(): """


@socketio.on('message')
def handleMessage(msg):
    print("Message: " + msg)
    send(msg, broadcast = True)

#Server
if __name__ == '__main__':
    socketio.run(app)
    #app.run(port = 3000, debug = True) #Debug = true is for restart the server automatically

