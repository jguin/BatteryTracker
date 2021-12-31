import time
import csv
from tkinter import *
from tkinter import messagebox
import pymysql
from sshtunnel import SSHTunnelForwarder
import pandas as pd


def get_tunnel():
    ssh_host = '192.168.86.22'
    ssh_port = 22
    ssh_user = 'pi'
    ssh_pw = 'raspberry'

    sql_hostname = '127.0.0.1'
    sql_port = 3306

    temp_tunnel = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_pw,
            remote_bind_address=(sql_hostname, sql_port))
    temp_tunnel.start()
    return temp_tunnel


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


class Application:
    def __init__(self, win, tun, maxid):
        self.sn = Label(win, text='Serial Number')
        self.snEntry = Entry(bd=3)
        self.sn.grid(column=0, row=0, padx=5, pady=5)
        self.snEntry.grid(column=1, row=0, padx=5, pady=5)
        self.max_sn = Label(win, text='Newest Cell ID: '+str(maxid))
        self.max_sn.grid(column=2, row=0, padx=5, pady=5)
        self.lookupButton = Button(win, text='Look Up', command=lambda: self.lookup(tun))
        self.clearButton = Button(win, text='Clear', command=self.clear)
        self.insertButton = Button(win, text='Insert', command=lambda: self.insert(tun))
        self.updateButton = Button(win, text='Update', command=lambda: self.update(tun))
        self.lookupButton.grid(column=0, row=1, padx=5, pady=5)
        self.clearButton.grid(column=1, row=1, padx=5, pady=5)
        self.insertButton.grid(column=2, row=1, padx=5, pady=5)
        self.updateButton.grid(column=2, row=10, padx=5, pady=5, rowspan=2)

        # Battery Make
        self.make = Label(win, text='Make')
        self.make.grid(column=0, row=2, padx=5, pady=5)
        self.makeEntry = Entry(bd=3)
        self.makeEntry.grid(column=1, row=2, padx=5, pady=5)

        # Battery Model
        self.model = Label(win, text='Model')
        self.model.grid(column=0, row=3, padx=5, pady=5)
        self.modelEntry = Entry(bd=3)
        self.modelEntry.grid(column=1, row=3, padx=5, pady=5)

        # Internal Resistance
        self.ir = Label(win, text='Internal Resistance')
        self.ir.grid(column=0, row=4, padx=5, pady=5)
        self.irEntry = Entry(bd=3)
        self.irEntry.grid(column=1, row=4, padx=5, pady=5)

        # Capacity
        self.capacity = Label(win, text='Capacity')
        self.capacity.grid(column=0, row=5, padx=5, pady=5)
        self.capacityEntry = Entry(bd=3)
        self.capacityEntry.grid(column=1, row=5, padx=5, pady=5)

        # Date Tested
        self.dateTested = Label(win, text='Date Tested')
        self.dateTested.grid(column=0, row=6, padx=5, pady=5)
        self.dateTestedButton = Button(win, text='Today', command=self.today_tested)
        self.dateTestedButton.grid(column=2, row=6, padx=5, pady=5)
        self.dateTestedEntry = Entry(bd=3)
        self.dateTestedEntry.grid(column=1, row=6, padx=5, pady=5)

        # Tested Voltage
        self.testedVoltage = Label(win, text='Tested Voltage')
        self.testedVoltage.grid(column=0, row=7, padx=5, pady=5)
        self.testedVoltageEntry = Entry(bd=3)
        self.testedVoltageEntry.grid(column=1, row=7, padx=5, pady=5)

        # Date Retested
        self.dateRetested = Label(win, text='Date Retested')
        self.dateRetested.grid(column=0, row=8, padx=5, pady=5)
        self.dateRetestedButton = Button(win, text='Today', command=self.today_retested)
        self.dateRetestedButton.grid(column=2, row=8, padx=5, pady=5)
        self.dateRetestedEntry = Entry(bd=3)
        self.dateRetestedEntry.grid(column=1, row=8, padx=5, pady=5)

        # Retested Voltage
        self.retestedVoltage = Label(win, text='Retested Voltage')
        self.retestedVoltage.grid(column=0, row=9, padx=5, pady=5)
        self.retestedVoltageEntry = Entry(bd=3)
        self.retestedVoltageEntry.grid(column=1, row=9, padx=5, pady=5)

        # Valid Cell
        self.valid = Label(win, text='Valid Cell?')
        self.valid.grid(column=0, row=10, padx=5, pady=5)
        self.validCheck = Checkbutton()
        self.validCheck.grid(column=1, row=10, padx=5, pady=5)

        # In Service
        self.inService = Label(win, text='In Service?')
        self.inService.grid(column=0, row=11, padx=5, pady=5)
        self.inServiceCheck = Checkbutton()
        self.inServiceCheck.grid(column=1, row=11, padx=5, pady=5)

    def lookup(self, tun):
        sn = self.snEntry.get()
        self.clear()
        data = query_db(tun, sn, 1, [])
        if data:
            self.snEntry.insert(0, data[0][0])
            self.makeEntry.insert(0, data[0][1])
            self.modelEntry.insert(0, data[0][2])
            self.irEntry.insert(0, data[0][3])
            self.capacityEntry.insert(0, data[0][4])
            self.dateTestedEntry.insert(0, data[0][5])
            self.testedVoltageEntry.insert(0, data[0][6])
            self.dateRetestedEntry.insert(0, data[0][7])
            self.retestedVoltageEntry.insert(0, data[0][8])
        else:
            messagebox.showerror(title='Error', message='Serial number entered does not exist')

    def clear(self):
        self.snEntry.delete(0, 'end')
        self.makeEntry.delete(0, 'end')
        self.modelEntry.delete(0, 'end')
        self.irEntry.delete(0, 'end')
        self.capacityEntry.delete(0, 'end')
        self.dateTestedEntry.delete(0, 'end')
        self.testedVoltageEntry.delete(0, 'end')
        self.dateRetestedEntry.delete(0, 'end')
        self.retestedVoltageEntry.delete(0, 'end')

    def insert(self, tun):
        # Check is SN exists
        sn = self.snEntry.get()
        lookup = query_db(tun, sn, 1, [])
        # If it does, tell user to update the record
        if lookup:
            messagebox.showerror(title='Error', message='Record already exists. Please lookup and update record')
            self.clear()
        # If it doesnt INSERT
        else:
            data = [sn, self.makeEntry.get(), self.modelEntry.get(), self.irEntry.get(), self.capacityEntry.get(),
                    self.dateTestedEntry.get(), self.testedVoltageEntry.get(), self.dateRetestedEntry.get(),
                    self.retestedVoltageEntry.get()]
            query_db(tun, sn, 2, data)
            self.max_sn['text'] = "Newest Cell ID: " + sn
            messagebox.showinfo(title='Insert', message='Record successfully inserted')

    def today_tested(self):
        today = time.strftime("%Y-%m-%d")
        self.dateTestedEntry.delete(0, 'end')
        self.dateTestedEntry.insert(0, today)

    def today_retested(self):
        today = time.strftime("%Y-%m-%d")
        self.dateRetestedEntry.delete(0, 'end')
        self.retestedVoltageEntry.delete(0, 'end')
        self.dateRetestedEntry.insert(0, today)

    def update(self, tun):
        # Check is SN exists
        sn = self.snEntry.get()
        if sn != "":
            lookup = query_db(tun, sn, 1, [])
            # If it does, update the record
            if lookup:
                data = [sn, self.makeEntry.get(), self.modelEntry.get(), self.irEntry.get(), self.capacityEntry.get(),
                        self.dateTestedEntry.get(), self.testedVoltageEntry.get(), self.dateRetestedEntry.get(),
                        self.retestedVoltageEntry.get()]
                query_db(tun, sn, 3, data)
                messagebox.showinfo(title='Update', message='Record successfully updated')
            # If it doesn't tell user to use INSERT
            else:
                messagebox.showerror(title='Error', message='Record does not exists. Please insert record')
        else:
            cells = query_db(tun, sn, 5, [])
            cell_string = ''
            if len(cells) > 0:
                for i in range(0, len(cells)):
                    cell_string = cell_string + str(cells[i][0]) + ", "
                cell_string = cell_string[:-2]
                messagebox.showinfo(title='Update', message='Cells needing update: ' + cell_string)
            else:
                messagebox.showinfo(title='Update', message='All cells are up to date')


def get_max_id(tun):
    data = query_db(tun, 0, 4, [])
    return data[0][0]


def bulk_load(tun):
    with open('cells.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8], row[9]]
            print(data)
            query_db(tun, row[0], 2, data)
            time.sleep(0.5)


window = Tk()
tunnel = get_tunnel()
max_id = get_max_id(tunnel)
window.columnconfigure(2)
window.rowconfigure(12)
application = Application(window, tunnel, max_id)
window.title('18650 Data Lookup')
window.geometry("375x425+10+10")
window.mainloop()
