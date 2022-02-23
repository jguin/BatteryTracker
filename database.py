from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas as pd
import csv
import time


def get_tunnel():
    ssh_host = '192.168.86.22'
    ssh_port = 22
    ssh_user = 'pi'
    ssh_pw = 'raspberry'

    sql_hostname = '127.0.0.1'
    sql_port = 3306

    tunnel = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_pw,
            remote_bind_address=(sql_hostname, sql_port))
    tunnel.start()
    return tunnel


def query_db(q_tunnel, sn, query_type, data):
    sql_username = 'user'
    sql_password = 'password'
    sql_main_database = '18650cells'

    conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                           passwd=sql_password, db=sql_main_database,
                           port=q_tunnel.local_bind_port)
    # Type 1: SELECT
    # Type 2: INSERT
    # Type 3: UPDATE
    # Type 4: Max ID
    # Type 5: Cells needing update
    if query_type == 1:
        sql = "SELECT * FROM cellData WHERE serialNumber = " + sn + ";"
        output = pd.read_sql_query(sql, conn)
        data_list = output.values.tolist()
        conn.close()
        return data_list
    elif query_type == 2:
        with conn:
            with conn.cursor() as cursor:
                sql = "INSERT INTO `cellData` (`serialNumber`, `make`, `model`, `ir`, `capacity`, `dateTested`, " \
                      "`voltageTested`, `dateRetested`, `voltageRetested`) VALUES ('" + data[0] + "', '" + data[1] + \
                      "', '" + data[2] + "', '" + data[3] + "', '" + data[4] + "', '" + data[5] + "', '" + data[6] + \
                      "', '" + data[7] + "', '" + data[8] + "');"
                cursor.execute(sql)
            conn.commit()
    elif query_type == 3:
        with conn:
            with conn.cursor() as cursor:
                sql = "UPDATE `cellData` SET `make` = '" + data[1] + "', `model` = '" + data[2] + \
                      "', `ir` = '" + data[3] + "', `capacity` = '" + data[4] + "', `dateTested` = '" + \
                      data[5] + "', `voltageTested` = '" + data[6] + "', `dateRetested` = '" + data[7] + \
                      "', `voltageRetested` = '" + data[8] + "' WHERE `cellData`.`serialNumber` = " + sn + ";"
                cursor.execute(sql)
                conn.commit()
    elif query_type == 4:
        sql = "SELECT MAX(serialNumber) FROM cellData;"
        output = pd.read_sql_query(sql, conn)
        data_list = output.values.tolist()
        conn.close()
        return data_list
    elif query_type == 5:
        sql = "SELECT `serialNumber` FROM `cellData` WHERE `dateRetested` = '' AND " \
              "DATEDIFF(CURRENT_DATE, `dateTested`) >= 14"
        output = pd.read_sql_query(sql, conn)
        data_list = output.values.tolist()
        conn.close()
        return data_list


def repacker_range_query(q_tunnel, start, end):
    sql_username = 'user'
    sql_password = 'password'
    sql_main_database = '18650cells'

    conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                           passwd=sql_password, db=sql_main_database,
                           port=q_tunnel.local_bind_port)
    sql = "SELECT serialNumber, capacity FROM cellData WHERE serialNumber >= " + str(start) + " and serialNumber <= " \
          + str(end) + ";"
    output = pd.read_sql_query(sql, conn)
    data_list = output.values.tolist()
    conn.close()
    return data_list

def bulk_load(tun):
    with open('cells.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8], row[9]]
            print(data)
            query_db(tun, row[0], 2, data)
            time.sleep(0.5)


def get_max_id(tun):
    data = query_db(tun, 0, 4, [])
    return data[0][0]
