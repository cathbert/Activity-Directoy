import os, sqlite3
from subprocess import call
from resources_and_tools.Logger import LoggerEngine

"""Each value stored in an SQLite database (or manipulated by the database engine) has one of the following storage classes:
           NULL.    The value is a NULL value.
           INTEGER. The value is a signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
           REAL.    The value is a floating point value, stored as an 8-byte IEEE floating point number.
           TEXT.    The value is a text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE).
           BLOB.    The value is a blob of data, stored exactly as it was input.
        """
log = LoggerEngine()


class Database:
    def __init__(self, *args, **kwargs):

        if not os.path.exists("database files"):
            log.log_warning(f"Database directory not found!")
            os.mkdir("database files")
            log.log_info(f"Database directory created successfully!")
            if not os.path.exists("database files/actidia.db"):
                log.log_warning(f"Database not found!")
                self.conn = sqlite3.connect("database files/actidia.db")
                self.cur = self.conn.cursor()
                self.cur.execute("CREATE TABLE IF NOT EXISTS user(fname TEXT ,"
                                 "lname TEXT, username TEXT, password TEXT)")
                self.cur.execute("CREATE TABLE IF NOT EXISTS activities(title TEXT ,"
                                 "time BLOB)")
                self.cur.execute("INSERT INTO user(fname, lname, username, password)"
                                 " VALUES(?,?,?,?)", ("Neziswa", 'Mutaurwa', "Nezi", "1"))
                self.conn.commit()
                log.log_info(f"Database and tables created successfully!")
        else:
            self.conn = sqlite3.connect("database files/actidia.db")
            self.cur = self.conn.cursor()

    def login_user(self, password):
        try:
            users = self.cur.execute("SELECT * FROM user WHERE password=?", (password,))

            for user in users.fetchall():
                if user[-1] == password:
                    log.log_info(f"Starting program USER: {user[0]} {user[1]}")
                    # Hiding directory
                    call(["attrib", "+H", "temporary_files"])
                    with open("temporary_files/current_user.txt", 'w') as f:
                        f.write(user[0] + " " + user[1])
                    return True
                else:
                    return False

        except Exception as e:
            print('Error', str(e))

    def register_new_user(self, firstname, lastname, username, password):
        self.cur.execute("INSERT INTO users(fname, lname, username, password)VALUES(?,?,?,?)",
                         (firstname, lastname, username, password))
        self.conn.commit()

    def get_all_users(self):
        all_users = self.cur.execute("SELECT * FROM users")
        return all_users.fetchall()

    def delete_user(self, name):
        self.cur.execute("DELETE FROM users WHERE fname=?", (name,))
        self.conn.commit()

    def clear_temporary(self):
        try:
            with open("temporary_files/current_user.txt", 'w') as f:
                f.write("")

        except Exception as e:
            print('Error', str(e))

    def __del__(self):
        self.cur.close()
        self.conn.close()
