import sqlite3

class DB:
    def __init__(self):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        self.conn = conn
        self.cursor = cursor
        cursor.execute('''CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                                tel_id VARCHAR[15], 
                                                                name VARCHAR[20],
                                                                sname VARCHAR[20],
                                                                phone VARCHAR[13],
                                                                mail VARCHAR[40],
                                                                type INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                                schedule TEXT,
                                                                teacher_id INTEGER, 
                                                                duration INTEGER, 
                                                                name VARCHAR[40])''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS link_group (group_id INTEGER,
                                                                student_id INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS honors (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            description TEXT,
                                                            image_link TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS people_with_honors (student_id INTEGER,
                                                            honor_id INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS list_types (type_id SMALLINT,
                                                                type_name VARCHAR[20])''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS admin (login VARCHAR[40],
                                                                        password VARCHAR[40])''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS saved_files (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                        fileName VARCHAR[50],
                                                                        binaryData VARBINARY[MAX])''')

        conn.commit()

    def add_to_base(self, ids, fname, scname, phone, mail):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO people (tel_id, name, sname, phone, mail, type) VALUES (?,?,?,?,?, NULL)''', (ids, fname, scname, phone, mail))
        conn.commit()
        conn.close()

    def save_file_to_db(self, name_file, file_id):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO saved_files (fileName, binaryData) VALUES(?, ?)", (name_file, file_id))
        conn.commit()
        conn.close()

    def get_all_achivment(self, chat_id):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute("Select id from people where tel_id = ?", [chat_id])
        current = cursor.fetchone()
        stud_id = str(current[0])
        cursor.execute("Select h.image_link from people_with_honors pwh" +
                       " JOIN honors h on pwh.honor_id = h.id where student_id = ?", [stud_id])
        honor_list = cursor.fetchall()
        return honor_list

    def add_student(self,tel_id,name,sname,phone, type):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO people VALUES (NULL,?,?,?,?,NULL,?)''', (tel_id,name,sname,phone, type))
        conn.commit()

    def get_student(self,chat_id):
        conn1 = sqlite3.connect('main.db')
        cursor1 = conn1.cursor()
        cursor1.execute('select name from people where tel_id = ?', [chat_id])
        res = cursor1.fetchone()[0]
        conn1 = sqlite3.connect('main.db')
        cursor1 = conn1.cursor()
        cursor1.execute('select sname from people where tel_id = ?', [chat_id])
        res1 = cursor1.fetchone()[0]

        return res + " "+ res1

    def get_admin_data(self, login, password):
        conn1 = sqlite3.connect('main.db')
        cursor1 = conn1.cursor()
        cursor1.execute('SELECT * FROM admin WHERE login=? AND password=?', (login, password))
        res = cursor1.fetchall()
        conn1.close()
        if res:
            return True
        else:
            return False

    def set_admin(self, telegram_id):
        conn1 = sqlite3.connect('main.db')
        cursor1 = conn1.cursor()
        print("db")
        print(telegram_id)
        cursor1.execute('''UPDATE people SET type = 1 where tel_id = ?''', [telegram_id])
        conn1.commit()
        conn1.close()

    def get_admin(self, telegram_id):
        conn1 = sqlite3.connect('main.db')
        cursor1 = conn1.cursor()
        cursor1.execute('SELECT * FROM people WHERE tel_id =? AND type = 1', [telegram_id])
        res = cursor1.fetchall()
        conn1.close()
        if res:
            return True
        else:
            return False

    def find_teacher_for_work(self,id):
        conn1 = sqlite3.connect('main.db')
        cursor1 = conn1.cursor()
        cursor1.execute('select tel_id from people left JOIN groups on groups.teacher_id = people.id where groups.id =?', [id])
        res = cursor1.fetchall()
        return res

db_object = DB()