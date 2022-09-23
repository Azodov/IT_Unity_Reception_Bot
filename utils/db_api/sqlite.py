import sqlite3


class Database:
    def __init__(self, path_to_db="ITUnityDB.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            user_id int NOT NULL,
            phonenumber varchar(15) NOT NULL,
            username varchar(255),
            fullname varchar(255),
            course varchar(255) NOT NULL,
            lang varchar(255) NOT NULL,
            age int NOT NULL,
            familyinfo varchar(255) NOT NULL
            );
"""
        self.execute(sql, commit=True)

    def create_table_course(self):
        sql = """
        CREATE TABLE Course (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name_uz varchar(255) NOT NULL,
            course_name_ru varchar(255) NOT NULL,
            course_name_en varchar(255) NOT NULL,
            course_bio_uz varchar(255),
            course_bio_ru varchar(255),
            course_bio_en varchar(255)
            );
"""
        self.execute(sql, commit=True)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, user_id: int,
                 phonenumber: str,
                 username: str,
                 fullname: str,
                 course: str,
                 lang: str,
                 age: int,
                 familyinfo: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(user_id,
        phonenumber,
        username,
        fullname,
        course,
        lang,
        age,
        familyinfo) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id,
                                      phonenumber,
                                      username, fullname,
                                      course,
                                      lang,
                                      age,
                                      familyinfo), commit=True)

    def add_course(self,
                   course_name_uz: str,
                   course_name_ru: str,
                   course_name_en: str,
                   course_bio_uz: str = None,
                   course_bio_ru: str = None,
                   course_bio_en: str = None,
                   ):
        # SQL_EXAMPLE = "INSERT INTO Course(course_id, course_name, course_bio) VALUES(1, 'Python', 'Bio uchin maydon')"

        sql = """
        INSERT INTO Course(
        course_name_uz,
        course_name_ru,
        course_name_en,
        course_bio_uz,
        course_bio_ru,
        course_bio_en) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(course_name_uz,
                                      course_name_ru,
                                      course_name_en,
                                      course_bio_uz,
                                      course_bio_ru,
                                      course_bio_en), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    # def update_user_email(self, email, id):
    #     # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"
    #
    #     sql = f"""
    #     UPDATE Users SET course=? WHERE user_id=?
    #     """
    #     return self.execute(sql, parameters=(course, user_id), commit=True)

    def delete_course(self):
        self.execute("DELETE FROM Course WHERE TRUE", commit=True)

    def get_courses(self):
        return self.execute("SELECT * FROM Course", fetchall=True)

    def course_detail_uz(self, course_name: str):
        query = self.execute("SELECT course_bio_uz FROM Course WHERE course_name_uz=?", parameters=(course_name,), fetchone=True)
        return query

    def course_detail_ru(self, course_name: str):
        query = self.execute("SELECT course_bio_ru FROM Course WHERE course_name_ru=?", parameters=(course_name,), fetchone=True)
        return query

    def course_detail_en(self, course_name: str):
        query = self.execute("SELECT course_bio_en FROM Course WHERE course_name_en=?", parameters=(course_name,), fetchone=True)
        return query


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
