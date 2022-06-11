from flask import Flask, request # kita akan pakai flask untuk membuat API
import os # ini untuk mendapatkan environment variable
from dotenv import load_dotenv
from flask_socketio import SocketIO
from routes import UserRoute as Users , AirConditionerRoute as AcRoute

load_dotenv() # func untuk membaca .env file
app = Flask(__name__) # pasang flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio = SocketIO(app,cors_allowed_origins='*',logger=True,async_mode='eventlet',async_handlers=True)
user_connected = 0

# For API
# example penjelasan Route Flask
@app.route('/users_find',methods=["POST"]) # ini adalah untuk mengatur route address
def user_find(): # func ini yang akan di execute kalau api manggil route diatas
    return Users.UserFindById(request.form.get('id')) # ini dari UserRoute

@app.route('/users_all',methods=["GET"])
def get_all_users():
    return Users.UserGetAll()
    
@app.route('/users_new',methods=["POST"])
def new_users():
    return Users.NewUsers(request.form.to_dict())

@app.route('/users_delete',methods=["POST"])
def delete_users():
    return Users.DeleteUsers(request.form.get('id'))

# Routes for Air Conditioner
# start-region
@app.route('/ac_running',methods=["POST"]) # ini untuk IOT ( Air Conditioner )
def ac_run():
    return AcRoute.RunningDevice(device_id=request.form.get('device_id'),socket=socketio)

@app.route('/stop_running',methods=["POST"]) # ini untuk IOT ( Air Conditioner )
def ac_stop():
    return AcRoute.StopDevice(device_id=request.form.get('device_id'),socket=socketio)

@app.route('/all_ac',methods=["GET"]) # ini untuk applikasi
def get_all_ac():
    return AcRoute.AllDevice()
    
@app.route('/ac_callback_running',methods=["POST"]) # ini untuk applikasi
def ac_callback_run():
    return AcRoute.CallbackEventDevice(device_id=request.form.get('device_id'),status=request.form.get('status'),message=request.form.get('message'),socket=socketio)
# end-region

@socketio.on('disconnect')
def test_disconnect():
    global user_connected
    user_connected -= 1
    print(f'Client disconnected, jumlah users = {user_connected}')

@socketio.on('connect')
def handle_connect():
    global user_connected
    user_connected += 1
    print(f"dapetin informasi {request.sid} jumlah users = {user_connected}")

socketio.run(app,'0.0.0.0',port=os.getenv('DEV_PORT'),debug=True)
# app.run(host=os.getenv('DEV_HOST'), port=os.getenv('DEV_PORT'), debug=True) # jalankan flask nya ( aktifkan kalau socket di off kan )