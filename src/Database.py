import sqlite3


class Database:
    def __init__(self, database_path: str):
        self.conn = sqlite3.connect(database=database_path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS USERS (id BIGINT PRIMARY KEY, name VARCHAR(64) NOT NULL, date_join DATE, id_proxy BIGINT REFERENCES PROXY(id) NOT NULL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS CONSIGNE (id integer PRIMARY KEY AUTOINCREMENT, id_user BIGINT REFERENCES USERS(id), consigne VARCHAR(255))")
        self.cur.execute(" CREATE TABLE IF NOT EXISTS PROXY (id integer PRIMARY KEY AUTOINCREMENT, ip VARCHAR(255) NOT NULL, port VARCHAR(255) NOT NULL, username VARCHAR(255), password VARCHAR(255))")
        self.conn.commit()

    def clear(self):
        self.cur.execute("DELETE FROM USERS")
        self.cur.execute("DELETE FROM CONSIGNE")
        self.conn.commit()

    def get_user(self, id):
        if self.cur.execute("SELECT * FROM USERS WHERE id=?", (id,)).fetchone() is None:
            return False
        return True

    def add_user(self, id, name):
        id_proxy = self.cur.execute("SELECT MAX(id_proxy) FROM USERS").fetchone()[0]
        if id_proxy is None:
            id_proxy = 1
        id_proxy += 1
        self.cur.execute("INSERT INTO USERS VALUES (?, ?,CURRENT_DATE, ?)", (id, name, id_proxy))
        self.conn.commit()

    def add_proxy(self, ip, port, username, password):
        self.cur.execute("INSERT INTO PROXY(ip, port, username, password) VALUES (?, ?, ?, ?)", (ip, port, username, password))
        self.conn.commit()

    def remove_user(self, id):
        self.cur.execute("DELETE FROM USERS WHERE id=?", (id,))
        self.conn.commit()

    def add_consigne(self, id_user, consigne):
        self.cur.execute("INSERT INTO CONSIGNE(id_user, consigne) VALUES (?, ?)", (id_user, consigne))
        self.conn.commit()

    def assign_proxy_to_users(self):
        self.cur.execute("SELECT id FROM USERS")
        users = self.cur.fetchall()
        self.cur.execute("SELECT id FROM PROXY")
        proxies = self.cur.fetchall()
        if len(users) > len(proxies):
            for i in range(len(proxies)):
                self.cur.execute("UPDATE USERS SET id_proxy=? WHERE id=?", (proxies[i][0], users[i][0]))
        else:
            for i in range(len(users)):
                self.cur.execute("UPDATE USERS SET id_proxy=? WHERE id=?", (proxies[i][0], users[i][0]))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

