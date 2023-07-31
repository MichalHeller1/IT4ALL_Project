from DB_Access import db_access
from DB_connection import connection

sqlCreateClientTable = """
    CREATE TABLE Client(
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name varchar(32),
    Address varchar(50),
    Phone varchar(17),
    Email varchar(30)
    )
"""

sqlCreateTechnicianTable = """
    CREATE TABLE Technician(
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name varchar(32),
    Password varchar(100),
    Phone varchar(17),
    Email varchar(30)
    )
"""

cursor = connection.cursor()
cursor.execute(sqlCreateTechnicianTable)


