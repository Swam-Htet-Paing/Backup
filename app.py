import logging
from flask import render_template, Flask,  request, Response, jsonify, session
import cv2
import requests
from flask_mysqldb import MySQL
import MySQLdb.cursors
from ultralytics import YOLO
import serial
# ser = serial.Serial('/dev/ttyACM0', baudrate=9600)
# def sendCmd(command):
#    ser.write(command.encode('utf-8'))

def send(command):
    try:
        response = requests.get(f"http://{ESP8266_IP}/{command}")
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

app = Flask(__name__)

# Code for disabling log messages outputting in the terminal
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'swam'
app.config['MYSQL_PASSWORD'] = 'swam123'
app.config['MYSQL_DB'] = 'iotDB1'
global_password = 'hellouser'

mysql = MySQL(app)
ESP8266_IP = "172.18.120.105"
ESP_PORT = 8080 
received = False
model = YOLO('./yolov5/runs/detect/train2/weights/last.pt')

def gen_frames():
  cap = cv2.VideoCapture(0)
  while True:
    success, frame = cap.read()
    if not success:
      break
      
      
    results = model(frame, verbose=False)[0]
    for result in results.boxes.data.tolist():
        x, y, x1, y1, score, class_id = result
        if score:
            cv2.rectangle(frame, (int(x), int(y)), (int(x1), int(y1)), (255,0,255), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1.3, (255,0,255), 3, cv2.LINE_AA)   
    success, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
           
@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    global received
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form["username"]
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password))
        account = cursor.fetchone()
        if account:
            return render_template('move.html')
        else:
            msg = "Incorrect password or username"
    return render_template('index.html', msg=msg)
@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       username = request.form['username']
       password = request.form['password']
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
       account = cursor.fetchone()
       
       if account:
          msg = 'Account with the name % s already exists', username
       
       else:
          cursor.execute('INSERT INTO users (username, password) VALUES (% s, % s)', (username, password, ))
          mysql.connection.commit()
          msg = 'Registration Completed!'       
    return render_template('index.html', msg=msg)

def send(command):
    try:
        response = requests.get(f"http://{ESP8266_IP}/{command}")
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# def Command(command):
#     print("received command " + command)
@app.route('/<command>', methods=['POST'])
def handle_command(command):
    send(command)
    # sendCmd(command)
    global received
    received = True
    # sendCmd(command)
    # command = request.form.get('command')

    # if not command:
    #     return "Missing command!", 400

    # # Send a POST request to the NodeMCU with the command
    # url = f"http://{NODEMCU_IP}/command"
    # try:
    #     response = requests.post(url, data={'command': command})
    #     response.raise_for_status()  # Raise an exception for non-2xx status codes
    received = False
    return "Command sent successfully!"
    # except requests.exceptions.RequestException as e:
    #     print(f"Error sending command: {e}")
    #     return "Failed to send command!", 500

if __name__ == "__main__":
  app.run(debug=True)

@app.route('/video_feed/')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

  # Build the URL to send the command to the ESP8266
  
    
if __name__ == '__main__':
   app.run()
