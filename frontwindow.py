import tkinter as tk
from tkinter import messagebox
from dataCollection import inputMode, is_float, is_alphabet
import datetime
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
    def __init__(self, master, expenseDict, depositDict):
        super().__init__(master)
        
        # Create and pack the label
        tk.Label(self, text="Expenses and Income:").grid(row = 0, column = 0)
        
        tk.Label(self, text="SubCategory:").grid(row = 0, column = 1)
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
                  command=lambda: master.switch_frame(ResultPage)).grid(row=4, column = 1)
        tk.Button(self, text="Submit",
                  command=lambda: self.submit).grid(row=4, column = 0)
        self.entry1 = tk.Entry(self, fg="grey")
        self.placeholder_text = "Source"
        self.entry1.insert(0, self.placeholder_text)
        self.entry1.grid(row=3, column=0)

        self.entry2 = tk.Entry(self, fg="grey")
        self.placeholder_text2 = "Value"
        self.entry2.insert(0, self.placeholder_text2)
        self.entry2.grid(row=3, column=1)

        self.entry1.bind("<FocusIn>", self.clear_placeholder)
        self.entry1.bind("<FocusOut>", self.set_placeholder)

        self.entry2.bind("<FocusIn>", self.clear_placeholder)
        self.entry2.bind("<FocusOut>", self.set_placeholder)

    def clear_placeholder(self, event):
        entry = event.widget
        """Clear placeholder text when the entry gets focus."""
        if entry.get() == self.placeholder_text or entry.get() == self.placeholder_text2:
            entry.delete(0, tk.END)
            entry.config(fg='black')  # Set text color to black for user input
    
    def set_placeholder(self, event):
        entry = event.widget
        if entry.get() == "":
            if entry is self.entry1:
                entry.insert(0, self.placeholder_text)
            else:
                entry.insert(0, self.placeholder_text2)
            entry.config(fg="grey")
    def update_categories(self, *args):
        selection = self.selected_option.get()
        
        # Show appropriate menu based on selection
        if selection == "Deposit":
            self.deposit_menu.grid(row=1, column=1)
            self.expenses_menu.grid_forget()
        elif selection == "Withdraw":
            self.expenses_menu.grid(row=1, column=1)
            self.deposit_menu.grid_forget()
    def submit(self):
        pass
class EnterPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        # Label above the entry box
        tk.Label(self, text="Enter the Date in YYYYMMDD:").pack(side="top", fill="x", pady=10)
        
        # Entry widget with placeholder text
        self.entry = tk.Entry(self)
        self.placeholder_text = "YYYYMMDD"
        self.entry.insert(0, self.placeholder_text)
        self.entry.pack(pady=5)
        
        # Set placeholder text color to grey
        self.entry.config(fg='grey')
        
        # Bind events for clearing and resetting placeholder text
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.set_placeholder)
        
        # Submit button
        tk.Button(self, text="Submit", command=self.submit).pack(pady=10)
    
    def clear_placeholder(self, event):
        """Clear placeholder text when the entry gets focus."""
        if self.entry.get() == self.placeholder_text:
            self.entry.delete(0, tk.END)
            self.entry.config(fg='black')  # Set text color to black for user input
    
    def set_placeholder(self, event):
        """Set placeholder text if the entry is empty when losing focus."""
        if self.entry.get() == "":
            self.entry.insert(0, self.placeholder_text)
            self.entry.config(fg='grey')  # Set placeholder color to grey
    
    def submit(self):
        data = self.entry.get()
        if self.is_valid_date(data):
            expense, deposit = inputMode(data)
            self.master.switch_frame(StartPage, expense, deposit)    
        else:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid date in YYYYMMDD format.")
    def is_valid_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False


class ResultPage(tk.Frame):
    def __init__(self, master, data=None):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is ResultPage").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Day's Results").pack()
        tk.Button(self, text="Categories's Results").pack()
        tk.Button(self, text="Exit Program", command=self.quit).pack(side="bottom", fill= "x", pady=10)
if __name__ == "__main__":
    app = SampleApp()
    app.update_idletasks()
    app.mainloop()
        