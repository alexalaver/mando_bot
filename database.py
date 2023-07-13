import psycopg2

class Data:
    def __init__(self, host, port, database, user, password):
        self.connect = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connect.cursor()

    def add_user(self, id, first_name, username):
        with self.connect:
            self.cursor.execute("INSERT INTO users(id, first_name, username) VALUES(%s, %s, %s)", (id, first_name, username,))
            self.connect.commit()

    def get_user(self, id):
        with self.connect:
            self.cursor.execute("SELECT id FROM users WHERE id=%s", (id,))
            return bool(len(self.cursor.fetchall()))


    def get_lang(self, id):
        with self.connect:
            self.cursor.execute("SELECT lang FROM users WHERE id=%s", (id,))
            return self.cursor.fetchone()[0]

    def get_cashe(self, id):
        with self.connect:
            self.cursor.execute("SELECT colum, texts FROM cashe WHERE id=%s", (id,))
            return self.cursor.fetchone()

    def set_lang(self, id, lang):
        with self.connect:
            self.cursor.execute("UPDATE users SET lang=%s WHERE id=%s", (lang, id,))
            self.connect.commit()

    def get_texts(self, user_id, texts):
        with self.connect:
            query = "SELECT {}, users.id, users.lang FROM texts, users WHERE users.id=%s AND texts.id=users.lang;".format(texts)
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()[0]

    def add_column(self, name):
        with self.connect:
            query = "ALTER TABLE texts ADD {} TEXT".format(name)
            self.cursor.execute(query)
            self.connect.commit()

    def get_column(self, column):
        with self.connect:
            query = f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'texts' AND column_name = '{column}'
            """
            self.cursor.execute(query)
            return bool(len(self.cursor.fetchall()))


    def del_column(self, name):
        with self.connect:
            query = "ALTER TABLE texts DROP COLUMN {}".format(name)
            self.cursor.execute(query)
            self.connect.commit()

    def add_column_option(self, name, texts, lang):
        with self.connect:
            a = "UPDATE texts SET {}=%s WHERE id=%s".format(name)
            self.cursor.execute(a, (texts, lang,))
            self.connect.commit()

    def add_cashe(self, id):
        with self.connect:
            self.cursor.execute("INSERT INTO cashe(id) VALUES(%s)", (id,))
            self.connect.commit()

    def update_cashe_column(self, id, colum):
        with self.connect:
            self.cursor.execute("UPDATE cashe SET colum=%s WHERE id=%s", (colum, id,))
            self.connect.commit()

    def update_cashe_text(self, id, text):
        with self.connect:
            self.cursor.execute("UPDATE cashe SET texts=%s WHERE id=%s", (text, id,))
            self.connect.commit()

    def update_cashe_lang(self, id, lang):
        with self.connect:
            self.cursor.execute("UPDATE cashe SET lang=%s WHERE id=%s", (lang, id,))
            self.connect.commit()

    def delete_cashe(self, id):
        with self.connect:
            self.cursor.execute("DELETE FROM cashe WHERE id=%s", (id,))
            self.connect.commit()


    def get_lvl(self, id):
        with self.connect:
            self.cursor.execute("SELECT lvl FROM users WHERE id=%s", (id,))
            return self.cursor.fetchone()[0]

    def add_orders(self, id, first_name, username, orders_text):
        with self.connect:
            self.cursor.execute("INSERT INTO users(id, first_name, username, orders_text) VALUES(%s, %s, %s, %s)", (id, first_name, username, orders_text,))
            self.connect.commit()

