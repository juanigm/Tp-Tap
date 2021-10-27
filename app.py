from flask import Flask, render_template, request
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
@app.route('/users', methods=['GET'])
def users():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuario')
    data = cursor.fetchall()
    print(data)
    return render_template('index.html', users = data)

@app.route('/chat', methods=['POST'])
def chats():
    if request.method == 'POST':
        myMessage = request.form['myMessage']
        print(myMessage)
       # cursor = mysql.connection.cursor()
        #cursor.execute('INSERT INTO mensaje (mensaje) VALUES (%s)', (myMessage))
        #mysql.connection.commit()
    return render_template('chats.html')

@socketio.on('message')
def handleMessage(msg):
    print("Message: " + msg)
    send(msg, broadcast = True)

#Server
if __name__ == '__main__':
    socketio.run(app)
    #app.run(port = 3000, debug = True) #Debug = true is for restart the server automatically

