from utils import Respon as respon
from database import connect_to_db,connect
db = connect_to_db

class ac_controller():
    
    def all_device(self):
        # ambil semua IOT yang terdaftar. check connection = 1 ( device terhubung ke server )
        db.execute("SELECT * FROM air_conditioner WHERE connection=1")
        data = db.fetchall()
        connect.commit()
        return respon.response_success(data)
    
    def running_device(self,device_id,socket):
        """
        Parameter
        -------- 
        - device_id    : `device_id` adalah nilai dari id yang terdapat pada row `table air_conditioner`, device_id pada func bersifat `required`
        
        Example
        -------
        >>> running = running_device(device_id=1)
        """
        
        db.execute("SELECT * FROM air_conditioner WHERE id = %s",(device_id,)) # panggil table buat dapet detail
        data = db.fetchone() # keluarin detail => type Object
        connect.commit()
        if(data): # check dlu kalau yg dicari ada, biar socket ga failure
            if(data['status'] == 0): # check kalau AC sedang tidak aktif
                socket.emit(f"event_ac_device_{data['id']}",{'message':'running','event': 1}) # kirim socket ke device dengan id yang di input, lalu data = 1 (berarti ingin di aktifkan)
                return respon.response_success(data)
            else:
                return respon.response_error("Air Conditioner sedang aktif !")
        else:
            return respon.response_error("Data yang anda cari tidak ditemukan !")
        
    def stop_device(self,device_id,socket):
        """
        Parameter
        -------- 
        - device_id    : `device_id` adalah nilai dari id yang terdapat pada row `table air_conditioner`, device_id pada func bersifat `required`
        
        Example
        -------
        >>> stop = stop_device(device_id=1)
        """
        
        db.execute("SELECT * FROM air_conditioner WHERE id = %s",(device_id,)) # panggil table buat dapet detail
        data = db.fetchone() # keluarin detail => type Object
        connect.commit()
        if(data): # check dlu kalau yg dicari ada, biar socket ga failure
            # if(data['status'] == 1): # check kalau AC sedang aktif
                socket.emit(f"event_ac_device_{data['id']}",{'message':'stoping','event': 0}) # kirim socket ke device dengan id yang di input, lalu data = 1 (berarti ingin di non aktifkan)
                return respon.response_success(data)
            # else:
            #     return respon.response_error("Air Conditioner sedang non aktif !")
        else:
            return respon.response_error("Data yang anda cari tidak ditemukan !")
        
    def callback_events(self,device_id,status,message,socket):
        """
        Parameter
        -------- 
        - device_id    : `device_id` adalah nilai dari 'column id' yang terdapat pada row `table air_conditioner`, device_id pada func bersifat `required`
        - status       : `status` adalah nilai dari `column status` yang terdapat pada row `table air_conditioner`, status pada func bersifat `required`
        - message      : `message` adalah pesan balikan dari socket, nilai pada message default hanya akan bernilai `running` atau `stoping`
        - socket       : `socket` adalah methods socket yang akan digunakan untuk mengeksekusi socket, socket pada func bersifat `required`
        
        Example
        -------
        >>> callback = callback_running(device_id=1,status=1,message='stoping',socket=socketio)
        """
        
        # kirim socket dari IOT ke semua applikasi yang aktif
        socket.emit(f'callback_run_device_{device_id}',{'message':message,'event': status})
        # setelah berhasil di kirim socket, update table air_conditioner pada column status dan check berdasarkan id
        db.execute("UPDATE air_conditioner SET status = %s WHERE id = %s",(status,device_id))
        connect.commit() # simpan
        
        return respon.response_success("data berhasil di update")
