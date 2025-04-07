import os.path
import sqlite3
from sqlite3 import Error
import os
from flask_bcrypt import check_password_hash

PATH_DB_TABLES = os.path.abspath(os.path.dirname(__file__)) + "/databases"


class StudyRoomDB:
    def __init__(self):
        db_connect = open_connection("studyroom")
        self.courses = get_all_courses(db_connect)
        if self.courses is None or len(self.courses) == 0:
            raise IndexError("Insert course into database!")
        db_connect.close()


def create_connection(path: str):
    """Open path as a database"""
    connection = None
    try:
        # Försöker du koppla till en fil som inte finns,
        # skapar sqlite3.connect en ny fil enligt "path"
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful!")
    except Error as e:
        print(f"The error {e} occurred!")
    return connection


def open_connection(db: str):
    return create_connection(os.path.join(PATH_DB_TABLES, db + ".db"))


def execute_read_query(connection, query: str, limit: int = None):
    """Use this function to read data from database"""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        if limit is None:
            result = cursor.fetchall()
        else:
            result = cursor.fetchmany(limit)
        return result
    except Error as e:
        print(f"The error {e} occurred!")


def get_all_courses(connection):
    """Use this function to return all courses from database table courses"""
    query = """SELECT * FROM courses;"""
    return execute_read_query(connection, query)


def get_course_with_id(connection, course_id):
    """Use this function to return course info from database table courses"""
    query = f"""SELECT * FROM courses WHERE course_id='{course_id}';"""
    return execute_read_query(connection, query)


def get_quest_for_id(connection, course_id):
    """Use this function to return all questions related to course id"""
    query = f"""SELECT * FROM quizes WHERE course_id='{course_id}' ORDER BY RANDOM();"""
    return execute_read_query(connection, query)


def execute_query(connection, query: str):
    """Use this function to insert data to database"""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Error as e:
        print(f"The error {e} occurred!")


def insert_query(connection, table, value_ids, values):
    """Use this function to insert data to database"""
    query = f"""INSERT OR IGNORE INTO {table} {value_ids} VALUES {values};"""

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error {e} occurred!")


def user_is_valid(connection, username, password) -> bool:
    """ Use function to check if a user exist in the database of users"""
    query = f"SELECT * FROM admin_user WHERE username='{username}'"
    users = execute_read_query(connection, query)

    for user in users:
        hashed_password = user[2]
        if check_password_hash(hashed_password, password):
            print('success')
            print(user[2])
            print(password)
            return True
        else:
            print('fail')
            print(user[2])
            print(password)
            return False


def init_studyroom_db():
    """ Initiates a new database for studyroom website"""
    connection = open_connection("studyroom")

    query = """
            CREATE TABLE IF NOT EXISTS quizes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            topic TEXT NOT NULL, 
            question TEXT NOT NULL, 
            answer TEXT NOT NULL);
            """

    execute_query(connection, query)

    query = """
            CREATE TABLE IF NOT EXISTS courses(
            course_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            info TEXT NOT NULL);
            """

    execute_query(connection, query)

    query = """
                CREATE TABLE IF NOT EXISTS topics(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                name TEXT NOT NULL);
                """

    execute_query(connection, query)

    insert_query(connection, "courses", "(course_id, name, info)",
                 """
                 ('EDA231', 'Programming Intro', 'Denna kurs gäller för programmeringsspråket Python och täcker dessa ämnen: <br>
                 Programmeringsspråks datatyper och dess användning <br>
                 Hur programmeringsspråket kan hantera datalagring <br>
                 Programmeringsspråkets kontrollstrukturer <br>
                 Programmeringsspråkets grundläggande datastrukturer <br>
                 Vanliga verktyg som används för programutveckling, enhetstestning och versionshantering <br>
                 Agila arbetsformer Kunna på ett grundläggande sätt tillämpa <br>
                 Programmeringsspråkets paradigmer och en korrekt programstruktur'), 
                 ('EDA233', 'Computer Networks', 'Denna kurs täcker följande ämnen: <br> 
                 Redogöra grundläggande begrepp, referensmodeller och säkerhetsaspekter inom datorkommunikation<br> 
                 Funktioner, egenskaper och samband för datakommunikation inom IoT<br>
                 Trådlösa tekniker<br> 
                 MQTT<br> 
                 Olika bibliotek <br>
                 För-och nackdelar med trådad eller trådlös teknik Färdigheter om/i<br>
                 Hantera utrustning för utvecklingsarbete med hjälp av verktyg och metoder <br>
                 Kunna lösa ett givet problem utifrån en kravspecifikation <br> 
                 På svenska och engelska kunna presentera, planera och utvärdera egna och andras lösningar och arbete <br> 
                 Tillämpa kunskaper i datorkommunikation för att felsöka nätverk med inbyggda system och kringutrustning'),
                 ('EDA234', 'Computer Security', 'Denna kurs täcker följande ämnen: <br> 
                 Innebörden om modern IT-säkerhet och särskilda aspekter inom säkerhet som tillämpas inom IoT <br>
                 Säkerhets- och etikfrågor inom IoT <br>
                 Grundläggande krypteringsalgoritmers funktion och betydelse <br>
                 Vanligt förekommande säkerhetsrisker mot informationsintensiva system inom IoT-tillämpningar samt hur 
                 man kan arbeta proaktivt för att motverka dessa säkerhetsrisker <br> 
                 Skydd av hårdvara och system <br>
                 Vanligt förekommande begrepp och metoder inom området, till exempel: VPN, IPsec, WEP, kryptoalgoritmer och kryptoanalys <br>
                 Lagar och regler: GDPR'),
                 ('EDA235', 'Datastructures & Algorithms', 'Denna kurs täcker följande ämnen: <br> 
                 Begreppen abstrakt datatyp, rekursion och komplexitet <br> 
                 Hur algoritmer definieras och byggs upp för att lösa definierade problem <br>
                 Användningen av tekniker för algoritmdesign på diskreta problem'),
                 ('EDA236', 'Cloud & Edge Computing', 'Denna kurs täcker följande ämnen: <br>
                 Nätverk <br> 
                 Virtualisering <br> 
                 Terminologier och definitioner <br> 
                 Molntjänster <br> 
                 Molnets uppbyggnad och Edge Computing <br> 
                 Olika teknikers för- och nackdelar')
                 """)

    insert_query(connection, "topics", "(course_id, name)",
                 """
                 ((SELECT course_id FROM courses WHERE name='Computer Security'), 'Encryption'),
                 ((SELECT course_id FROM courses WHERE name='Computer Security'), 'Ethics and GDPR'),
                 ((SELECT course_id FROM courses WHERE name='Computer Security'), 'Malware')
                 """)

    insert_query(connection, "quizes", "(course_id, topic, question, answer)",
                 """
                 ('EDA231', 'None', 'Nämn tre olika datatyper.', 'Int, String, List, Dictionary, osv.'),
                 ('EDA233', 'None', 'Vilket lager tillhör protokollet TCP enligt OSI-modellen?', 'Transport'), 
                 ('EDA234', 'None', 'Vad betyder asymmetrisk kryptering?', 'Kryptering och avkryptering sker med olika nycklar'),
                 ('EDA234', 'None', 'Vilket protokoll för WiFi-säkerhet är mest önskvärd att använda idag?', 'WPA3'),
                 ('EDA234', 'None', 'Vilken kryptografisk standard rekommenderas idag för symmetrisk kryptering?', 'AES'),
                 ('EDA234', 'None', 'Vad står CIA för?', 'Confidentiality Integrity Availability'),
                 ('EDA234', 'None', 'Pelle skickar medvetet ett mail till sin Säpo polare Johans jobbdator med ett malware i. Vilken terminologi passar bäst in i vad Pelle gör?', 'Attack'),
                 ('EDA234', 'None', 'Vad är CVE?', 'En databas med upptäckta sårbarigheter.'),
                 ('EDA234', 'None', 'Vad är "Day 0"?', 'Första dagen då en sårbarhet har påträffats'),
                 ('EDA234', 'None', 'Vilken är INTE en förekommande cyberattack? Port Scan, SYN-Flooding, Ping of Death', 'Port Scan'),
                 ('EDA235', 'None', 'Nämn två olika sorters länkade listor.', 'Dubbel-länkad lista, Cirkulär-länkad lista'),
                 ('EDA235', 'None', 'Vad är den asymtotiska komplexiteten (värsta fallet) av att lägga till 1 element i en Stack av storlek M, baserad på en Länkad Lista?', 'O(1)'),
                 ('EDA235', 'None', 'Vad är den asymtotiska komplexiteten (värsta fallet) av att lägga till N element i en Stack av storlek M, baserad på en Länkad Lista?', 'O(1)'),
                 ('EDA236', 'None', 'Vad kallas ramverket som vi bygger en hemsida i Python?', 'Flask')
                 """)


def main():
    print(PATH_DB_TABLES)
    init_studyroom_db()


if __name__ == '__main__':
    main()
