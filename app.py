from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

#Conection from bd
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tp_tap'

mysql = MySQL(app)


#Routes
@app.route('/')
def Index():
    return 'Hello World'


#Server
if __name__ == '__main__':
    app.run(port = 3000, debug = True) #Debug = true is for restart the server automatically

