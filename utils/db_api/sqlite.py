import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
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
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
        """
        self.execute(sql, commit=True)

    def create_categroy_table(self):
        sql = """
        CREATE TABLE Category (
            id INTEGER PRIMARY KEY,
            title VARCHAR(55) NOT NULL
        );
        """
        self.execute(sql=sql, commit=True)
    
    def create_secondary_category_table(self):
        sql = """
        CREATE TABLE SecondaryCategory (
            id INTEGER PRIMARY KEY,
            title VARCHAR(55) NOT NULL,
            cat_id INTEGER NOT NULL
        );
        """
        self.execute(sql=sql, commit=True)
    
    def create_product_table(self):
        sql = """
        CREATE TABLE Product (
            id INTEGER PRIMARY KEY,
            title VARCHAR(55) NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            price REAL NOT NULL,
            secondary_cat_id INTEGER NOT NULL
        );
        """
        self.execute(sql=sql, commit=True)

    def create_user_cart_table(self):
        sql = """
        CREATE TABLE Cart (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        );
        """
        self.execute(sql=sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)
    
    def add_cart(self, user_id, product_id, quantity):
        sql = """
        INSERT INTO Cart(user_id, product_id, quantity) VALUES(?, ?, ?);
        """
        self.execute(sql=sql, parameters=(user_id, product_id, quantity), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user_cart(self, **kwargs):
        sql = """
        SELECT * FROM Cart WHERE
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_cats(self):
        sql = """
        SELECT * FROM Category
        """
        return self.execute(sql=sql, fetchall=True)

    def select_cat(self, **kwargs):
        sql = """
        SELECT * FROM Category WHERE
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def select_secondary_cats(self, **kwargs):
        sql = """
        SELECT * FROM SecondaryCategory WHERE
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_secondary_cat(self, **kwargs):
        sql = """
        SELECT * FROM SecondaryCategory WHERE
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_products(self, **kwargs):
        sql = """
        SELECT * FROM Product WHERE
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)
    
    def select_product(self, **kwargs):
        sql = """
        SELECT * FROM Product WHERE
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)
    
    def update_user_cart(self, user_id, product_id, quantity):
        sql = f"""
        UPDATE Cart SET quantity=? WHERE user_id=? AND product_id=?
        """
        self.execute(sql, parameters=(quantity, user_id, product_id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)
    
    def clear_cart(self, **kwargs):
        sql = """
        DELETE FROM Cart WHERE
        """
        sql, parameters = self.format_args(sql, kwargs)
        self.execute(sql, parameters=parameters, commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
