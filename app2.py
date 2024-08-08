from flask import render_template, Flask,  request, Response, jsonify, session
import cv2
import requests
from flask_mysqldb import MySQL
import MySQLdb.cursors
import serial
from ultralytics import YOLO
ser = serial.Serial('/dev/ttyACM0', baudrate=9600)


def sendCmd(command):
   ser.write(command.encode('utf-8'))

# def send(command):
#     try:
#         response = requests.get(f"http://{ESP8266_IP}/{command}")
#         print(response.text)
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'swam'
app.config['MYSQL_PASSWORD'] = 'swam123'
app.config['MYSQL_DB'] = 'iotDB1'
global_password = 'hellouser'
mysql = MySQL(app)
ESP8266_IP = "172.18.72.51"
ESP_PORT = 8080

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
    if request.method == 'POST' and 'password' in request.form:
        password = request.form['password']
        if password == global_password:
           return render_template('move.html')
        else:
            msg = "Incorrect password or username"
    return render_template('index2.html', msg=msg)

@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
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
          return render_template('login.html', msg=msg)       
    return render_template('index.html', msg=msg)

@app.route('/<command>', methods=['POST'])
def handle_command(command):
    sendCmd(command)
    return "Command sent successfully!"
   
if __name__ == "__main__":
  app.run(debug=True)

@app.route('/video_feed/')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

  # Build the URL to send the command to the ESP8266
  
    
if __name__ == '__main__':
   app.run()
