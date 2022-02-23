import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import database
import repacker
import tkinter as tk


class DatabaseData:
    def __init__(self, win, tun, maxid):
        self.sn = Label(win, text='Serial Number')
        self.snEntry = Entry(win, bd=3)
        self.sn.grid(column=0, row=0, padx=5, pady=5)
        self.snEntry.grid(column=1, row=0, padx=5, pady=5)
        self.max_sn = Label(win, text='Newest Cell ID: '+str(maxid))
        self.max_sn.grid(column=2, row=0, padx=5, pady=5)
        self.lookupButton = Button(win, text='Look Up', command=lambda: self.lookup(tun))
        self.clearButton = Button(win, text='Clear', command=self.clear)
        self.insertButton = Button(win, text='Insert', command=lambda: self.insert(tun))
        self.updateButton = Button(win, text='Update', command=lambda: self.update_cell(tun))
        self.lookupButton.grid(column=0, row=1, padx=5, pady=5)
        self.clearButton.grid(column=1, row=1, padx=5, pady=5)
        self.insertButton.grid(column=2, row=1, padx=5, pady=5)
        self.updateButton.grid(column=2, row=10, padx=5, pady=5, rowspan=2)

        # Battery Make
        self.make = Label(win, text='Make')
        self.make.grid(column=0, row=2, padx=5, pady=5)
        self.makeEntry = Entry(win, bd=3)
        self.makeEntry.grid(column=1, row=2, padx=5, pady=5)

        # Battery Model
        self.model = Label(win, text='Model')
        self.model.grid(column=0, row=3, padx=5, pady=5)
        self.modelEntry = Entry(win, bd=3)
        self.modelEntry.grid(column=1, row=3, padx=5, pady=5)

        # Internal Resistance
        self.ir = Label(win, text='Internal Resistance')
        self.ir.grid(column=0, row=4, padx=5, pady=5)
        self.irEntry = Entry(win, bd=3)
        self.irEntry.grid(column=1, row=4, padx=5, pady=5)

        # Capacity
        self.capacity = Label(win, text='Capacity')
        self.capacity.grid(column=0, row=5, padx=5, pady=5)
        self.capacityEntry = Entry(win, bd=3)
        self.capacityEntry.grid(column=1, row=5, padx=5, pady=5)

        # Date Tested
        self.dateTested = Label(win, text='Date Tested')
        self.dateTested.grid(column=0, row=6, padx=5, pady=5)
        self.dateTestedButton = Button(win, text='Today', command=self.today_tested)
        self.dateTestedButton.grid(column=2, row=6, padx=5, pady=5)
        self.dateTestedEntry = Entry(win, bd=3)
        self.dateTestedEntry.grid(column=1, row=6, padx=5, pady=5)

        # Tested Voltage
        self.testedVoltage = Label(win, text='Tested Voltage')
        self.testedVoltage.grid(column=0, row=7, padx=5, pady=5)
        self.testedVoltageEntry = Entry(win, bd=3)
        self.testedVoltageEntry.grid(column=1, row=7, padx=5, pady=5)

        # Date Retested
        self.dateRetested = Label(win, text='Date Retested')
        self.dateRetested.grid(column=0, row=8, padx=5, pady=5)
        self.dateRetestedButton = Button(win, text='Today', command=self.today_retested)
        self.dateRetestedButton.grid(column=2, row=8, padx=5, pady=5)
        self.dateRetestedEntry = Entry(win, bd=3)
        self.dateRetestedEntry.grid(column=1, row=8, padx=5, pady=5)

        # Retested Voltage
        self.retestedVoltage = Label(win, text='Retested Voltage')
        self.retestedVoltage.grid(column=0, row=9, padx=5, pady=5)
        self.retestedVoltageEntry = Entry(win, bd=3)
        self.retestedVoltageEntry.grid(column=1, row=9, padx=5, pady=5)

        # Valid Cell
        self.valid = Label(win, text='Valid Cell?')
        self.valid.grid(column=0, row=10, padx=5, pady=5)
        self.validCheck = Checkbutton(win)
        self.validCheck.grid(column=1, row=10, padx=5, pady=5)

        # In Service
        self.inService = Label(win, text='In Service?')
        self.inService.grid(column=0, row=11, padx=5, pady=5)
        self.inServiceCheck = Checkbutton(win)
        self.inServiceCheck.grid(column=1, row=11, padx=5, pady=5)

    def lookup(self, tun):
        sn = self.snEntry.get()
        self.clear()
        data = database.query_db(tun, sn, 1, [])
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
        lookup = database.query_db(tun, sn, 1, [])
        # If it does, tell user to update the record
        if lookup:
            messagebox.showerror(title='Error', message='Record already exists. Please lookup and update record')
            self.clear()
        # If it doesnt INSERT
        else:
            data = [sn, self.makeEntry.get(), self.modelEntry.get(), self.irEntry.get(), self.capacityEntry.get(),
                    self.dateTestedEntry.get(), self.testedVoltageEntry.get(), self.dateRetestedEntry.get(),
                    self.retestedVoltageEntry.get()]
            database.query_db(tun, sn, 2, data)
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

    def update_cell(self, tun):
        # Check is SN exists
        sn = self.snEntry.get()
        if sn != "":
            lookup = database.query_db(tun, sn, 1, [])
            # If it does, update the record
            if lookup:
                data = [sn, self.makeEntry.get(), self.modelEntry.get(), self.irEntry.get(), self.capacityEntry.get(),
                        self.dateTestedEntry.get(), self.testedVoltageEntry.get(), self.dateRetestedEntry.get(),
                        self.retestedVoltageEntry.get()]
                database.query_db(tun, sn, 3, data)
                messagebox.showinfo(title='Update', message='Record successfully updated')
            # If it doesn't tell user to use INSERT
            else:
                messagebox.showerror(title='Error', message='Record does not exists. Please insert record')
        else:
            cells = database.query_db(tun, sn, 5, [])
            cell_string = ''
            if len(cells) > 0:
                for i in range(0, len(cells)):
                    cell_string = cell_string + str(cells[i][0]) + ", "
                cell_string = cell_string[:-2]
                messagebox.showinfo(title='Update', message='Cells needing update: ' + cell_string)
            else:
                messagebox.showinfo(title='Update', message='All cells are up to date')


class Repacker:
    def __init__(self, win, tun):
        self.cell_variable = StringVar(win)
        self.cell_variable.set("Choose Cell...")
        self.options = ["Choose Cell..."]
        self.packs = []

        self.number_cells = Label(win, text='Number of cells')
        self.number_cells_entry = Entry(win, bd=3)
        self.number_cells.grid(column=0, row=0, padx=5, pady=5)
        self.number_cells_entry.grid(column=1, row=0, padx=5, pady=5)

        self.starting_sn = Label(win, text='Starting Serial Number')
        self.starting_sn_entry = Entry(win, bd=3)
        self.starting_sn.grid(column=0, row=1, padx=5, pady=5)
        self.starting_sn_entry.grid(column=1, row=1, padx=5, pady=5)

        self.ending_sn = Label(win, text='Ending Serial Number')
        self.ending_sn_entry = Entry(win, bd=3)
        self.ending_sn.grid(column=0, row=2, padx=5, pady=5)
        self.ending_sn_entry.grid(column=1, row=2, padx=5, pady=5)

        self.repack_button = Button(win, text='Repack', command=lambda: self.start_repack(tun, win))
        self.repack_button.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

        self.drop = OptionMenu(win, self.cell_variable, *self.options)
        self.drop.grid(column=0, row=4, padx=5, pady=5, sticky='w')

        self.serial_number_list = scrolledtext.ScrolledText(win, state='disabled', wrap=WORD, height=10, width=40)
        self.serial_number_list.grid(column=0, row=5, columnspan=2, padx=5, pady=5, sticky='w')

    def start_repack(self, tun, win):
        self.options.clear()
        num_cells = self.number_cells_entry.get()
        start_sn = self.starting_sn_entry.get()
        end_sn = self.ending_sn_entry.get()
        data = repacker.read_cells(tun, int(start_sn), int(end_sn))
        repacker.sort_cells(data)
        self.packs = repacker.build_pack(int(num_cells), data)
        for x in range(1, len(self.packs)+1):
            self.options.append(str(x))
        self.drop = OptionMenu(win, self.cell_variable, *self.options, command=self.display_selected_cell)
        self.drop.grid(column=0, row=4, padx=5, pady=5, sticky='w')

    def display_selected_cell(self, choice):
        choice = self.cell_variable.get()
        current_pack = self.packs[int(choice) - 1]
        total_cell_capacity = 0
        self.serial_number_list.configure(state='normal')
        self.serial_number_list.delete(1.0, END)
        for x in range(1, len(current_pack)):
            self.serial_number_list.insert(tk.INSERT, str(current_pack[x][0])+', ')
            total_cell_capacity += current_pack[x][1]
        self.serial_number_list.delete("end-3c", END)
        self.serial_number_list.insert(tk.INSERT, "\r\nTotal Capacity: " + str(total_cell_capacity))
        self.serial_number_list.configure(state='disabled')


window = Tk()
tunnel = database.get_tunnel()
max_id = database.get_max_id(tunnel)
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Cell Data')
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='Repacker')
DatabaseData(tab1, tunnel, max_id)
Repacker(tab2, tunnel)
tabControl.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')


window.title('18650 Data Lookup')
window.geometry("380x450+10+10")
window.mainloop()
