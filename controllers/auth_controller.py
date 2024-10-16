from models.user import User

class AuthController:
    @staticmethod
    def register_user(username, email, password):
        if User.get_user_by_username(username):
            return False, "Username already exists"
        User.create_user(username, email, password)
        return True, "User registered successfully"

    @staticmethod
    def login_user(username, password):
        if User.verify_password(username, password):
            User.update_last_login(username)
            return True, "Login successful"
        return False, "Invalid username or password"