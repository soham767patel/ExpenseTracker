import tkinter as tk
from tkinter import messagebox
from dataCollection import inputMode, is_float, is_alphabet, withdraw, deposit, saveData, showDataDay, showDataMonth, showDataYear
import datetime
from tkinter import *
from tkinter import font

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title("Expense Tracker")
        self.switch_frame(EnterPage)
        self.update_idletasks()
    def switch_frame(self, frame_class, *args):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, *args)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self.rowconfigure([0,1,2], weight = 1)
        self.columnconfigure(0, weight = 1)
        self._frame.grid(row = 0, column = 0, sticky = "nsew")
        self.update_idletasks()
class StartPage(tk.Frame):
    def __init__(self, master, expense, income, date):
        self.counter = 0
        super().__init__(master)
        self.expense2 = expense
        self.deposit2 = income
        self.rowconfigure([0,1,2,3,4], weight = 1)
        self.columnconfigure([0,1], weight = 2)
        # Create and grid the label
        self.entry3 = tk.Label(self, text="Expenses and Income:")
        self.entry3.grid(row = 0, column = 0, sticky = "nsew")
        self.counter_label = tk.Label(self, text=f'Submits Made: {self.counter}')
        self.counter_label.grid(row=0, column=1, sticky = "nsew")
        # Create StringVar for the main dropdown menu
        self.selected_option = tk.StringVar()
        self.selected_option.set("Deposit")  # default value
        
        # Create and grid the OptionMenu for main selection
        self.main_menu = tk.OptionMenu(self, self.selected_option, "Deposit", "Withdraw")
        self.main_menu.grid(row=1, column=0, sticky = "nsew")
        
        # Create StringVar for expenses and deposit categories
        self.expenses_var = tk.StringVar()
        self.deposit_var = tk.StringVar()
        
        # Example categories (should be defined in your actual code)
        self.expensesCategory = ["Housing", "Transportation", "Healthcare", "Education", "Entertainment and Leisure","Personal Care","Clothing","Insurance","Taxes","Miscellaneous"]
        self.depositCategory = ["Employment Income", "Self-Employment Income","Investment Income","Rental Income","Government Assistance","Other Income"]
        
        # Create and grid the OptionMenus for categories
        self.expenses_menu = tk.OptionMenu(self, self.expenses_var, *self.expensesCategory)
        self.deposit_menu = tk.OptionMenu(self, self.deposit_var, *self.depositCategory)
        
        # Set default values for category menus
        self.expenses_var.set(self.expensesCategory[0])
        self.deposit_var.set(self.depositCategory[0])
        
        # Update the categories based on the selected option
        self.selected_option.trace_add("write", self.update_categories)
        self.deposit_menu.grid(row=1, column=1, sticky = "nsew")
        # Button to switch to the ResultPage
        self.res = tk.Button(self, text="Open ResultPage",
                  command=lambda: master.switch_frame(ResultPage, self.expense2, self.deposit2, date))
        self.res.grid(row=4, column = 1, sticky = "nsew")
        self.sub = tk.Button(self, text="Submit",
                  command=lambda: self.submit(self.expense2, self.deposit2))
        self.sub.grid(row=4, column = 0, sticky = "nsew")
        self.entry1 = tk.Entry(self)
        self.placeholder_text = "Source"
        self.entry1.insert(0, self.placeholder_text)
        self.entry1.grid(row=3, column=0, sticky = "nsew")

        self.entry2 = tk.Entry(self)
        self.placeholder_text2 = "Value"
        self.entry2.insert(0, self.placeholder_text2)
        self.entry2.grid(row=3, column=1, sticky = "nsew")
        self.entry1.bind("<FocusIn>", self.clear_placeholder)
        self.entry1.bind("<FocusOut>", self.set_placeholder)
        
        self.entry2.bind("<FocusIn>", self.clear_placeholder)
        self.entry2.bind("<FocusOut>", self.set_placeholder)
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Update font size based on window size."""
        # Get window dimensions
        height = self.winfo_height()
        
        # Calculate a scaling factor based on window size
        # For example, font size could be based on height
        scale_factor = height / 20
        
        # Create a new font size
        new_font_size = int(scale_factor)
        
        # Create a font object with the new size
        new_font = font.Font(family="Helvetica", size=new_font_size)
        
        # Update the font of widgets
        self.entry3.config(font=new_font)
        self.counter_label.config(font=new_font)
        self.main_menu.config(font=new_font)
        self.deposit_menu.config(font=new_font)
        self.expenses_menu.config(font=new_font)
        self.entry1.config(font=new_font)
        self.entry2.config(font=new_font)
        self.res.config(font=new_font)
        self.sub.config(font=new_font)
    def clear_placeholder(self, event):
        entry = event.widget
    
        if entry.get() == self.placeholder_text or entry.get() == self.placeholder_text2:
            entry.delete(0, tk.END)
    
    def set_placeholder(self, event):
        entry = event.widget
        if entry.get() == "":
            if entry is self.entry1:
                entry.insert(0, self.placeholder_text)
            else:
                entry.insert(0, self.placeholder_text2)
    def update_categories(self, *args):
        selection = self.selected_option.get()
        
        # Show appropriate menu based on selection
        if selection == "Deposit":
            self.deposit_menu.grid(row=1, column=1)
            self.expenses_menu.grid_forget()
        elif selection == "Withdraw":
            self.expenses_menu.grid(row=1, column=1)
            self.deposit_menu.grid_forget()
    def submit(self, expense, income):
        source = self.entry1.get()
        value = self.entry2.get()
        expensesDict = {"Housing": 0, "Transportation": 1, "Healthcare": 2, "Education": 3, "Entertainment and Leisure": 4,"Personal Care": 5,"Clothing":6,"Insurance":7,"Taxes":8,"Miscellaneous":9}
        depositDict = {"Employment Income":0, "Self-Employment Income":1,"Investment Income":2,"Rental Income":3,"Government Assistance":4,"Other Income":5}
        if self.selected_option.get() == "Deposit":
            category = depositDict.get(self.deposit_var.get())
        else:
            category = expensesDict.get(self.expenses_var.get())
        if not is_alphabet(source):
            tk.messagebox.showerror("Invalid Input", "Please enter a valid source only letters and spaces allowed")
        elif not is_float(value):
            tk.messagebox.showerror("Invalid Input", "Please enter a valid amount of money")
        else:
            if self.selected_option.get() == "Withdraw":
                self.expense2 = withdraw(expense, category, source, value)
                self.counter+=1
                self.entry1.delete(0, tk.END)
                self.entry2.delete(0, tk.END)
            else:
                self.deposit2 = deposit(income, category, source, value)
                self.counter+=1
                self.entry1.delete(0, tk.END)
                self.entry2.delete(0, tk.END)
            self.counter_label.config(text=f'Submits Made: {self.counter}')           
class EnterPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg = "black")
       # super().__init__(master)
        self.rowconfigure([0,1,2], weight = 1)
        self.columnconfigure(0, weight = 1)
        # Label above the entry box
        self.top_label = tk.Label(self, text="Enter the Date in YYYYMMDD:", bg = "black", fg = "white")
        self.top_label.grid(row = 0, column = 0, pady=10, sticky = "nsew")

        # Entry widget with placeholder text
        self.entry1 = tk.Entry(self)
        self.placeholder_text = "YYYYMMDD"
        self.entry1.insert(0, self.placeholder_text)
        self.entry1.configure( bg = "black", fg = "white")
        self.entry1.grid(row = 1, column = 0, pady=5, sticky = "nsew")

        # Bind events for clearing and resetting placeholder text
        self.entry1.bind("<FocusIn>", self.clear_placeholder)
        self.entry1.bind("<FocusOut>", self.set_placeholder)

        # Submit button
        self.entry2 = tk.Button(self, text="Submit", command=self.submit, fg = "black")
        self.entry2.grid(row = 2, column = 0, pady=10, sticky = "nsew")

        self.bind("<Configure>", self.on_resize)
    def on_resize(self, event):
        """Update font size based on window size."""
        # Get window dimensions
        height = self.winfo_height()
        
        # Calculate a scaling factor based on window size
        # For example, font size could be based on height
        scale_factor = height / 20
        
        # Create a new font size
        new_font_size = int(scale_factor)
        
        # Create a font object with the new size
        new_font = font.Font(family="Helvetica", size=new_font_size)
        
        # Update the font of widgets
        self.top_label.config(font=new_font)
        self.entry1.config(font=new_font)
        self.entry2.config(font=new_font)
    def clear_placeholder(self, event):
        """Clear placeholder text when the entry gets focus."""
        entry = event.widget
        if entry.get() == self.placeholder_text:
            entry.delete(0, tk.END)
            entry.configure(bg = "grey", fg = "white")

    def set_placeholder(self, event):
        entry = event.widget
        """Set placeholder text if the entry is empty when losing focus."""
        if entry.get() == "":
            entry.insert(0, self.placeholder_text)
            entry.configure(bg = "black", fg = "white")


    def submit(self):
        date = self.entry1.get()
        if self.is_valid_date(date):
            # Assuming inputMode and StartPage are defined elsewhere
            self.expense, self.income = inputMode(date)
            self.master.switch_frame(StartPage, self.expense, self.income, date)    
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid date in YYYYMMDD format.")

    def is_valid_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False
class ResultPage(tk.Frame):
    def __init__(self, master, expense2, deposit2, date):
        saveData(expense2, deposit2, date)
        tk.Frame.__init__(self, master)
        self.rowconfigure([0,1,2,3,4,5,6], weight = 1)
        self.columnconfigure(0, weight = 1)
        date_str = date
        date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")
        currDate = date_obj.strftime("%Y-%m-%d")
        self.button1 = tk.Label(self, text=f"Today's Date: {currDate}")
        self.button1.grid(row = 0, column = 0, pady=10, sticky = "nwes")
        self.button2 =tk.Button(self, text="Day's Results", command=lambda: showDataDay(expense2, deposit2, date))
        self.button2.grid(row = 1, column = 0, pady=10, sticky = "nwes")
        self.button3 = tk.Button(self, text="Deposit's Results", command=lambda: master.switch_frame(DepositResultPage,date,expense2,deposit2))
        self.button3.grid(row = 2, column = 0, pady=10, sticky = "nwes")
        self.button4 =tk.Button(self, text="Expense's Results", command=lambda: master.switch_frame(ExpenseResultPage,date,expense2,deposit2))
        self.button4.grid(row = 3, column = 0, pady=10, sticky = "nwes")
        self.button5 =tk.Button(self, text="Month's Results", command=lambda: showDataMonth(date))
        self.button5.grid(row = 4, column = 0, pady=10, sticky = "nwes")
        self.button6 =tk.Button(self, text="Years's Results", command=lambda: showDataYear(date))
        self.button6.grid(row = 5, column = 0, pady=10, sticky = "nwes")
        self.button7 =tk.Button(self, text="Exit Program", command = self.quit)
        self.button7.grid(row = 6, column = 0, pady=10, sticky = "nwes")
        self.bind("<Configure>", self.on_resize)
    def on_resize(self, event):
        """Update font size based on window size."""
        # Get window dimensions
        height = self.winfo_height()
        
        # Calculate a scaling factor based on window size
        # For example, font size could be based on height
        scale_factor = height / 20
        
        # Create a new font size
        new_font_size = int(scale_factor)
        
        # Create a font object with the new size
        new_font = font.Font(family="Helvetica", size=new_font_size)
        
        # Update the font of widgets
        self.button1.config(font=new_font)
        self.button2.config(font=new_font)
        self.button3.config(font=new_font)
        self.button4.config(font=new_font)
        self.button5.config(font=new_font)
        self.button6.config(font=new_font)
        self.button7.config(font=new_font)
class DepositResultPage(tk.Frame):
    def __init__(self, master, date, expense, deposit):
        self.expense2 = expense
        self.deposit2 = deposit
        tk.Frame.__init__(self, master)
        depositCategory = ["Employment Income", "Self-Employment Income","Investment Income","Rental Income","Government Assistance","Other Income"]
        tk.Label(self, text=f"Deposit Results: {date}").grid(row = 0, column = 0, pady=10)
        for i, item in enumerate(depositCategory):
            tk.Button(self, text=f'{depositCategory[i]}', command=lambda num=i: showDataDay(self.expense2, self.deposit2, date, num, None, None, 1)).grid(column = 0, pady=10)
        tk.Button(self, text="Return", command=lambda: master.switch_frame(ResultPage, self.expense2, self.deposit2, date)).grid(column = 0, pady=10)
class ExpenseResultPage(tk.Frame):
    def __init__(self, master, date, expense, deposit):
        tk.Frame.__init__(self, master)
        self.expense2 = expense
        self.deposit2 = deposit
        expensesCategory = ["Housing", "Transportation", "Healthcare", "Education", "Entertainment and Leisure","Personal Care","Clothing","Insurance","Taxes","Miscellaneous"]
        tk.Label(self, text=f"Expense Results: {date}").grid(row = 0, column = 0, pady=10)
        for j, jtem in enumerate(expensesCategory):
            tk.Button(self, text=f'{expensesCategory[j]}', command=lambda num=j: showDataDay(self.expense2, self.deposit2, date, num, None, None, 2)).grid(column = 0, pady=10)
        tk.Button(self, text="Return", command=lambda: master.switch_frame(ResultPage, self.expense2, self.deposit2, date)).grid(column = 0, pady=10)
if __name__ == "__main__":
    app = SampleApp()
    app.update_idletasks()
    app.mainloop()
