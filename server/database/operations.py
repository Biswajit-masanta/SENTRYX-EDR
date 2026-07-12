from datetime import datetime
try:
    from .connection import get_connection
except ImportError:
    from connection import get_connection

def check_if_sys_info_exists(hostname):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT COUNT(*) FROM sys_info WHERE hostname = ?
    ''', (hostname,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def get_system_id(hostname):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id FROM sys_info WHERE hostname = ?
    ''', (hostname,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def insert_sys_info(system_info):
    if not(check_if_sys_info_exists(system_info.hostname)):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO sys_info (hostname, os_name, os_release, architecture, processor, cpu_count, python_version, last_seen) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (system_info.hostname, system_info.os_name, system_info.os_release, system_info.architecture, system_info.processor, system_info.cpu_count, system_info.python_version, system_info.last_seen))
        conn.commit()
        conn.close()
        print(f"New System added: {system_info.hostname}")
    else:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE sys_info
            SET last_seen = ?
            WHERE hostname = ?
        """, (system_info.last_seen, system_info.hostname))

    conn.commit()
    conn.close()

    print(f"Updated heartbeat: {system_info.hostname}")

def insert_resource_usage(system_id,resource_usage):
    conn = get_connection()
    cursor = conn.cursor()
    from datetime import datetime
    timestamp = str(datetime.now())
    cursor.execute('''
    INSERT INTO resource_usage (system_id, cpu_usage, memory_usage, disk_usage, timestamp) VALUES (?,?, ?, ?, ?)
    ''', (system_id,resource_usage.cpu_usage, resource_usage.memory_usage, resource_usage.disk_usage, timestamp))
    conn.commit()
    conn.close()

def insert_alert(system_id, severity ,alert_type ,status ,message ):
    conn = get_connection()
    cursor = conn.cursor()
    from datetime import datetime
    timestamp = str(datetime.now())
    cursor.execute('''
    INSERT INTO alert_table (system_id, severity , alert_type, status, message , timestamp ) values (?,?,?,?,?,?)
    ''', (system_id, severity ,alert_type, status ,message ,timestamp))
    conn.commit()
    conn.close()


def check_if_alert_exist(system_id, alert_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT COUNT(*)
    FROM alert_table
    WHERE system_id = ?
    AND alert_type = ?
    AND status = 'ACTIVE'
    ''', (system_id, alert_type))

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

def resolve_alert(system_id, alert_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE alert_table
    SET status = 'RESOLVED'
    WHERE system_id = ?
    AND alert_type = ?
    AND status = 'ACTIVE'
    ''', (system_id, alert_type))

    conn.commit()
    conn.close()


def get_all_resource_usage():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resource_usage")

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "system_id": row[1],
            "cpu_usage": row[2],
            "memory_usage": row[3],
            "disk_usage": row[4],
            "timestamp": row[5]
        })

    conn.close()

    return data

from datetime import datetime

def get_all_system():
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute("SELECT * FROM sys_info")
    data = []

    for row in rows:

        last_seen = datetime.fromisoformat(row[8])
        current_time = datetime.now()

        difference = (current_time - last_seen).total_seconds()

        if difference <= 30:
            status = "ONLINE"
        else:
            status = "OFFLINE"

        data.append({
            "id": row[0],
            "hostname": row[1],
            "os_name": row[2],
            "os_release": row[3],
            "architecture": row[4],
            "processor": row[5],
            "cpu_count": row[6],
            "python_version": row[7],
            "last_seen": row[8],
            "status": status
        })

    conn.close()
    return data

def get_all_alert():
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute("SELECT * FROM alert_table")

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "system_id": row[1],
            "severity": row[2],
            "alert_type": row[3],
            "status": row[4],
            "message": row[5],
            "timestamp": row[6]
        })

    conn.close()
    return data
def get_total_active_alerts(system_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM alert_table
        WHERE system_id = ?
        AND status = 'ACTIVE'
    """, (system_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total
def save_one_process(system_id, process):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO process_table (
            system_id,
            pid,
            process_name,
            exe_path,
            cpu_usage,
            memory_usage,
            status,
            risk_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        system_id,
        process.pid,
        process.process_name,
        process.exe_path,
        process.cpu_usage,
        process.memory_usage,
        process.status,
        "LOW"
    ))
    conn.commit()
    conn.close()


def get_all_process():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.system_id,
            p.pid,
            p.process_name,
            p.exe_path,
            p.cpu_usage,
            p.memory_usage,
            p.status,
            p.risk_level,
            p.timestamp,
            s.hostname
        FROM process_table p
        LEFT JOIN sys_info s
        ON p.system_id = s.id
    """)

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "system_id": row[1],
            "pid": row[2],
            "process_name": row[3],
            "exe_path": row[4],
            "cpu_usage": row[5],
            "memory_usage": row[6],
            "status": row[7],
            "risk_level": row[8],
            "timestamp": row[9],
            "hostname": row[10]
        })

    conn.close()
    return data


def update_process(system_id, process):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE process_table
        SET
            process_name = ?,
            exe_path = ?,
            cpu_usage = ?,
            memory_usage = ?,
            status = ?,
            risk_level = ?
        WHERE system_id = ?
        AND pid = ?
    """, (
        process.process_name,
        process.exe_path,
        process.cpu_usage,
        process.memory_usage,
        process.status,
        "LOW",
        system_id,
        process.pid
    ))

    conn.commit()
    conn.close()

def process_exists(system_id, pid):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM process_table
        WHERE system_id = ?
        AND pid = ?
    """, (system_id, pid))

    result = cursor.fetchone()

    conn.close()

    return result is not None

def delete_missing_processes(system_id, active_pids):
    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join("?" * len(active_pids))

    cursor.execute(f"""
        DELETE FROM process_table
        WHERE system_id = ?
        AND pid NOT IN ({placeholders})
    """, [system_id] + active_pids)

    conn.commit()
    conn.close()


def save_ml_prediction(system_id, prediction, confidence, model, version):
    conn = get_connection()
    cursor = conn.cursor()

    from datetime import datetime

    cursor.execute("""
        INSERT INTO ml_predictions
        (system_id, prediction, confidence, model, version, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        system_id,
        prediction,
        confidence,
        model,
        version,
        datetime.now()
    ))

    conn.commit()
    conn.close()

def get_latest_ml_prediction(system_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT prediction,
               confidence,
               model,
               version,
               timestamp
        FROM ml_predictions
        WHERE system_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (system_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "prediction": row[0],
        "confidence": row[1],
        "model": row[2],
        "version": row[3],
        "timestamp": row[4]
    }