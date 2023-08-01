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
#
# cursor = connection.cursor()
# cursor.execute(sqlCreateTechnicianTable)

sqlCreateNetworkTable = """
    CREATE TABLE Network(
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name varchar(32),
    Location varchar(100),
    Client int,
    FOREIGN KEY (Client) REFERENCES Client(id)
    )
    
"""

sqlCreateDeviceTable = """
    CREATE TABLE Device(
    MacAddress varchar(30) NOT NULL PRIMARY KEY,
    Provider varchar(32),
    Network int,
    FOREIGN KEY (Network) REFERENCES Network(id)
    )

"""

sqlCreateConnectionTable = """
    CREATE TABLE Connection(
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Protocol varchar(20),
    Source varchar(30) NOT NULL,
    Destination varchar(30) NOT NULL,
    FOREIGN KEY (Source) REFERENCES Device(MacAddress),
    FOREIGN KEY (Destination) REFERENCES Device(MacAddress)

    )

"""

sqlCreatePermissionsTable = """
    CREATE TABLE Permissions(
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Technician int,
    Client int,
    FOREIGN KEY (Technician) REFERENCES Technician(id),
    FOREIGN KEY (Client) REFERENCES Client(id)

    )

"""

insertTechnicians = """INSERT INTO Technician (
    Name,
    Password,
    Phone,
    Email
)
VALUES
    (   'Tovi',
        '$2a$12$TsB6KCgG8mytfjkZlXaVDeBJw1E56e7532r1mV.vpQRSqJdzZyFdG',
        '058-3232818',
        'Tovi@gmail.com'
    ),
    (   'Avia',
        '$2a$12$Q.jVmoZMMdNC0.kuq8phdum9I630ZbxM73xNNCn0pp/mba/q4v6wa',
        '052-4659745',
        'Avia@gmail.com'
    ),
    (   'Michal',
        '$2a$12$8VgZFDb9EM104KveiM5kI.Hs2PbdzEzySXkAMmYjW851ZnE1kGZg6',
        '055-6451874',
        'Michal@gmail.com'
    );"""

insertClients = """INSERT INTO Client (
    Name,
    Address,
    Phone,
    Email
)
VALUES
    (   'Shalom',
        'Jerusalem',
        '055-5555558',
        'Shalom@gmail.com'
    ),
    (   'Gadi',
        'Jerusalem',
        '055-5555559',
        'Avi@gmail.com'
    ),
    (   'Yoram',
        'Jerusalem',
        '055-5555552',
        'Yoram@gmail.com'
    );"""

insertPermissions = """INSERT INTO Permissions (
    Technician,
    Client
)
VALUES
    (   4,
        1
    ),
    (   4,
        2
    ),
    (   4,
        3
    ),
     (  5,
        1
    ),
    (   5,
        2
    ),
    (   5,
        3
    ),
     (  6,
        1
    ),
    (   6,
        2
    ),
    (   6,
        3
    );"""

with connection.cursor() as cursor:
    cursor.execute(insertPermissions)
    connection.commit()
