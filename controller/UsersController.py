from datetime import datetime
from mysql.connector.errors import IntegrityError
from utils import Respon as respon
import bcrypt
from database import connect_to_db,connect
db = connect_to_db

class users_controller():

    """
    Function
    -------- 
    Function yang tersedia memiliki balikan data row dan function yang dapat anda gunakan sebagai berikut :

    - `find_users`   : function untuk mencari data users pada row berdasarkan `id`, parameter yang ditetapkan adalah `id`. Memiliki
                        balikan data berupa `Object`
    - `get_all_users`: function untuk mencari semua data users pada row. Memiliki
                        balikan data berupa `Array`
    - `new_users`    : function untuk membuat data baru pada users. Memiliki
                        balikan data berupa `Object`. Check pada function `new_users` untuk melihat arguments
    - `deleted_users`: function untuk menghapus data pada users. Memiliki
                        balikan data berupa `String`
    
    
    Example
    -------
    >>> users = UsersController().find_users(id=10)
    >>> users = UsersController().get_all_users()
    >>> users = UsersController().new_users(data=form_data_user)
    >>> users = UsersController().deleted_users(id=1)
    """

    def get_all_users(self):
        db.execute("SELECT * FROM users")
        data = db.fetchall()
        connect.commit()
        return respon.response_success(data) if data else respon.response_success([])
    
    def find_users(self,id=int):
        """
        Parameter
        -------- 
        - id    : `id` adalah nilai dari id yang terdapat pada row, id pada func bersifat `required`
        
        Example
        -------
        >>> cari_users = find_users(10)
        """
        if not id: #validator
            return respon.response_error("ID is required !")
        
        db.execute("SELECT * FROM users WHERE id = %s",(id,))
        data = db.fetchone()
        connect.commit()
        return respon.response_success(data) if data else respon.response_error("Users yang anda cari tidak ditemukan !")
    
    def new_users(self,data):
        """
        Parameter
        -------- 
        - data    : `data` adalah value pada row users, data pada func bersifat `required`.
            
            information pada argumants `data` meliputi :
            
            - Required  : `first_name`,`last_name`,`email`,`password`,`gender`,`job`
            - Not Required  : `avatar`,`bio`,`age`,`number_phone`,`city`
        
        Example
        -------
        >>> new = new_users(data)
        """
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = bcrypt.hashpw(data.get('password').encode('utf-8'),bcrypt.gensalt(rounds=10))
        gender = data.get('gender')
        job = data.get('job')
        
        avatar = data.get('avatar') if data.get('avatar') else None 
        bio = data.get('bio') if data.get('bio') else None
        number_phone = data.get('number_phone') if data.get('number_phone') else None
        age = data.get('age') if data.get('age') else None
        city = data.get('city') if data.get('city') else None
        
        created_at = datetime.now()
        updated_at = datetime.now()

        try:
            db.execute("INSERT INTO users (first_name,last_name,email,password,gender,job,avatar,bio,age,number_phone,city,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    ,(first_name,last_name,email,password,gender,job,avatar,bio,age,number_phone,city,created_at,updated_at))
            connect.commit()
        except IntegrityError as e: # check kalau gagal di save
            if e.errno == 1062: # kalau email duplicate
                return respon.response_error("Email yang anda masukan sudah terdaftar !")
            elif e.errno == 1048: # kalau form required kurang
                return respon.response_error("Form yang anda masukan tidak lengkap, harap periksa kembali !")
        db.execute("SELECT * FROM users WHERE email = %s",(email,))
        user_info = db.fetchone()
        return respon.response_success(user_info)
    
    def updated_users(self,data):
        pass
    
    def deleted_users(self,id):
        """
        Parameter
        -------- 
        - id    : `id` adalah nilai dari id yang terdapat pada row, id pada func bersifat `required`
        
        Example
        -------
        >>> hapus_users = deleted_users(10)
        """
        if not id: # validator
            return respon.response_error("ID is required !")
        
        db.execute("SELECT * FROM users WHERE id = %s",(id,)) # cari users dulu
        find_first =  db.fetchone()
        
        if find_first:
            db.execute("DELETE FROM users WHERE id = %s",(id,)) # delete users
            connect.commit()
            return respon.response_success("Users berhasil di hapus !")
        else:
            return respon.response_error("Users yang anda hapus tidak terdaftar !")
        
        