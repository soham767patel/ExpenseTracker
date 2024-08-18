import tkinter as tk
from tkinter import messagebox
from dataCollection import inputMode, is_float, is_alphabet, withdraw, deposit, saveData, showDataDay
import datetime
import sv_ttk
import darkdetect
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title("Expense Tracker")
        self.geometry("400x300")
        self.switch_frame(EnterPage)
        self.update_idletasks()
    def switch_frame(self, frame_class, *args):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, *args)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        self.update_idletasks()
class StartPage(tk.Frame):
    def __init__(self, master, expense, income, date):
        self.counter = 0
        super().__init__(master)
        self.expense2 = expense
        self.deposit2 = income
        # Create and pack the label
        tk.Label(self, text="Expenses and Income:").grid(row = 0, column = 0)
        self.counter_label = tk.Label(self, text=f'Submits Made: {self.counter}')
        self.counter_label.grid(row=0, column=1)
        # Create StringVar for the main dropdown menu
        self.selected_option = tk.StringVar()
        self.selected_option.set("Deposit")  # default value
        
        # Create and pack the OptionMenu for main selection
        self.main_menu = tk.OptionMenu(self, self.selected_option, "Deposit", "Withdraw")
        self.main_menu.grid(row=1, column=0)
        
        # Create StringVar for expenses and deposit categories
        self.expenses_var = tk.StringVar()
        self.deposit_var = tk.StringVar()
        
        # Example categories (should be defined in your actual code)
        self.expensesCategory = ["Housing", "Transportation", "Healthcare", "Education", "Entertainment and Leisure","Personal Care","Clothing","Insurance","Taxes","Miscellaneous"]
        self.depositCategory = ["Employment Income", "Self-Employment Income","Investment Income","Rental Income","Government Assistance","Other Income"]
        
        # Create and pack the OptionMenus for categories
        self.expenses_menu = tk.OptionMenu(self, self.expenses_var, *self.expensesCategory)
        self.deposit_menu = tk.OptionMenu(self, self.deposit_var, *self.depositCategory)
        
        # Set default values for category menus
        self.expenses_var.set(self.expensesCategory[0])
        self.deposit_var.set(self.depositCategory[0])
        
        # Update the categories based on the selected option
        self.selected_option.trace_add("write", self.update_categories)
        self.deposit_menu.grid(row=1, column=1)
        # Button to switch to the ResultPage
        tk.Button(self, text="Open ResultPage",
                  command=lambda: master.switch_frame(ResultPage, self.expense2, self.deposit2, date)).grid(row=4, column = 1)
        tk.Button(self, text="Submit",
                  command=lambda: self.submit(self.expense2, self.deposit2)).grid(row=4, column = 0)
        self.entry1 = tk.Entry(self)
        self.placeholder_text = "Source"
        self.entry1.insert(0, self.placeholder_text)
        self.entry1.grid(row=3, column=0)

        self.entry2 = tk.Entry(self)
        self.placeholder_text2 = "Value"
        self.entry2.insert(0, self.placeholder_text2)
        self.entry2.grid(row=3, column=1)
        self.entry1.bind("<FocusIn>", self.clear_placeholder)
        self.entry1.bind("<FocusOut>", self.set_placeholder)
        
        self.entry2.bind("<FocusIn>", self.clear_placeholder)
        self.entry2.bind("<FocusOut>", self.set_placeholder)

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

        # Label above the entry box
        top_label = tk.Label(self, text="Enter the Date in YYYYMMDD:")
        top_label.pack(side="top", fill="x", pady=10)

        # Entry widget with placeholder text
        self.entry1 = tk.Entry(self)
        self.placeholder_text = "YYYYMMDD"
        self.entry1.insert(0, self.placeholder_text)
        self.entry1.pack(pady=5)

        # Bind events for clearing and resetting placeholder text
        self.entry1.bind("<FocusIn>", self.clear_placeholder)
        self.entry1.bind("<FocusOut>", self.set_placeholder)

        # Submit button
        self.entry2 = tk.Button(self, text="Submit", command=self.submit)
        self.entry2.pack(pady=10)

    def clear_placeholder(self, event):
        """Clear placeholder text when the entry gets focus."""
        entry = event.widget
        if entry.get() == self.placeholder_text:
            entry.delete(0, tk.END)

    def set_placeholder(self, event):
        entry = event.widget
        """Set placeholder text if the entry is empty when losing focus."""
        if entry.get() == "":
            entry.insert(0, self.placeholder_text)


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
        date_str = date
        date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")
        currDate = date_obj.strftime("%Y-%m-%d")
        tk.Label(self, text=f"Today's Date: {currDate}").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Day's Results", command=lambda: showDataDay(expense2, deposit2)).pack()
        tk.Button(self, text="Categories's Results").pack()
        tk.Button(self, text="Exit Program", command = self.quit).pack(side="bottom", fill= "x", pady=10)
if __name__ == "__main__":
    app = SampleApp()
    app.update_idletasks()
    sv_ttk.set_theme(darkdetect.theme())
    app.mainloop()
