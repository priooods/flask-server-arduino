from controller import UsersController # import users controller
users = UsersController.users_controller()  # definisi dari user controller

def UserGetAll():
    return users.get_all_users() # keluarin respon nya

def UserFindById(id):
    return users.find_users(id)

def NewUsers(data):
    return users.new_users(data)

def DeleteUsers(data):
    return users.deleted_users(data)