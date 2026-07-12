import sqlite3

try:
    from .connection import DB_PATH, get_connection
except ImportError:
    from connection import DB_PATH, get_connection


def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute('''

    CREATE TABLE IF NOT EXISTS sys_info (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        hostname TEXT,

        os_name TEXT,

        os_release TEXT,

        architecture TEXT,

        processor TEXT,

        cpu_count INTEGER,

        python_version TEXT,

        last_seen TEXT

    )

    ''')

    conn.commit()

    conn.close()



def create_resource_usage_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute('''

    CREATE TABLE IF NOT EXISTS resource_usage (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        system_id INTEGER,

        cpu_usage REAL,

        memory_usage REAL,

        disk_usage REAL,

        timestamp TEXT

    )

    ''')

    conn.commit()

    conn.close()

def create_alert_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS alert_table (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        system_id INTEGER,

        severity TEXT,

        alert_type TEXT,

        status TEXT,
        
        message TEXT,

        timestamp TEXT
    )
    ''')
    conn.commit()
    conn.close()

def create_process_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS process_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        system_id TEXT NOT NULL,

        pid INTEGER NOT NULL,
        process_name TEXT NOT NULL,
        exe_path TEXT,

        cpu_usage REAL DEFAULT 0,
        memory_usage REAL DEFAULT 0,

        status TEXT DEFAULT 'RUNNING',
        risk_level TEXT DEFAULT 'LOW',

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_table()

    create_resource_usage_table()

    create_process_table()

    create_alert_table()

    print("Database tables created successfully.")


def create_process_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS ml_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        system_id INTEGER NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        model TEXT NOT NULL,
        version TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY(system_id) REFERENCES sys_info(id)
    );
    ''')
    conn.commit()
    conn.close()
