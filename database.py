import sqlite3, time


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user):
        with self.connection:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS `users` (user_id INTEGER, refer_id INTEGER, regist_time TEXT, premium TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS `bots` (token TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS `group` (group_text TEXT, group_id TEXT, group_link TEXT)")
            return self.cursor.execute("SELECT * FROM `users` WHERE user_id = ?", (user, )).fetchone()


    def new_user(self, user, refer_id=None):
        with self.connection:
            struct = time.localtime(time.time())
            reg_time = time.strftime("%Y-%m-%d %H:%M:%S", struct)
            return self.cursor.execute('INSERT INTO `users` (`user_id`, `refer_id`, `regist_time`) VALUES (?,?,?)', (user, refer_id, reg_time,))
        
    def all_refer(self, user):
        with self.connection:
            return self.cursor.execute("SELECT count(user_id) FROM `users` WHERE refer_id = ?", (user, )).fetchone()[0]
        
    def all_user(self):
        with self.connection:
            return self.cursor.execute("SELECT count(user_id) FROM `users`").fetchone()[0]
        
    def all_premium(self):
        with self.connection:
            return self.cursor.execute("SELECT count(user_id) FROM `users` WHERE premium = 1").fetchone()[0]
        
    def add_group(self, link, id, name):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'group' VALUES (?, ?, ?)", (name, id, link,))
        
    def get_old_users(self, days):
        with self.connection:
            query = "SELECT count(user_id) FROM users WHERE (regist_time BETWEEN date('now', ?) AND date('now', '+1 day'))"
            params = (f'-{days} day',)
            return self.cursor.execute(query, params).fetchone()[0]
        
    def bot_update(self, token, link):
        with self.connection:
            self.cursor.execute("UPDATE bots SET token = ?, bot_link = ? WHERE check_bot = 5", (token, link,))