from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from datetime import datetime

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app, manage_session=False)

#Conection from bd
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Loreto18'
app.config['MYSQL_DB'] = 'tp-tap'

mysql = MySQL(app)


#Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        userid = request.form['userid']
        password = request.form['password']
        session['userid'] = userid
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userId, password FROM usuario WHERE userid = %s AND password = %s', (userid,password))
        data = cursor.fetchall()
        #print('DATA: '+str(data))
    if(data):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM sala')
        data = cursor.fetchall()
        #print(data)
        return render_template('salas.html', salas = data)
    else:
        return redirect(url_for('index'))

@app.route('/chat', methods=['GET','POST'])
def chat():
    data = ''
    if(request.method == 'POST'):
        room = request.form['room']
        session['room'] = room
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM sala WHERE idSala LIKE %s', [room])
        data = cursor.fetchall()
        print(data)
        
        if(data):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('login'))

        
    else:
        if(session.get('userid') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('login'))



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


#Socket
@socketio.on('join', namespace='/chat')
def join(message):
    mensaje = ''
    user = ''
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('userid') + ' Entró en la sala.'}, room=room)
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT mensaje, userId FROM mensaje WHERE idSala LIKE %s', [room])
    data = cursor.fetchall()
    print('DATA: '+str(data))
    for a in data:
        print(a[0])
        emit('status', {'msg': a[1] + ': ' + a[0]}, room=request.sid)
        

@socketio.on('text', namespace='/chat')
def text(message):
    
    userid = session.get('userid')
    room = session.get('room')
    message1 = message['msg']
    date = datetime.today()
    emit('message', {'msg': session.get('userid') + ': ' + message['msg']}, room=room)
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO mensaje (mensaje, fecha, idSala, userId) VALUES (%s, %s, %s, %s)', (message1, date, room, userid))
    mysql.connection.commit()


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    userid = session.get('userid')
    print(session.get('room'))
    print(session['userid'])
    leave_room(room)
    session.clear()
    emit('status', {'msg': userid + ' salió de la sala.'}, room=room)

#Server
if __name__ == '__main__':
    socketio.run(app)
    #app.run(port = 3000, debug = True) #Debug = true is for restart the server automatically

