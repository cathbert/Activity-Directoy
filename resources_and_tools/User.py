import os, sqlite3


class UserLogin:
    def login_user(self, username, password):
        try:
            conn = sqlite3.connect("database files/actidia.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")

            for user in cur.fetchall():
                if user[0] == username and user[-1] == password:
                    return True

            cur.close()

        except Exception as e:
            print('Error', str(e))


u = UserLogin()
w = u.login_user('1111')
print(w)
