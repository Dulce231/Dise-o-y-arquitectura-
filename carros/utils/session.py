class Session:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.user = None
            cls._instance.logged_in = False
        return cls._instance

    def login(self, user_data):
        self.user = user_data
        self.logged_in = True

    def logout(self):
        self.user = None
        self.logged_in = False

    def is_logged_in(self):
        return self.logged_in

    def get_user(self):
        return self.user

    def clear(self):
        self.logout()
