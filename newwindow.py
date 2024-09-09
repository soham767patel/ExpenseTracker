import customtkinter
import tkinter
import tkinter.messagebox
from dataCollection import (inputMode, is_float, is_alphabet, withdraw, deposit,
                             saveData, showDataDay, showDataMonth, showDataYear, delete)

class SampleApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.state('zoomed')
        self._frame = None
        self.title("MoneyMinder")
        self.switch_frame(StartPage)
        self.update_idletasks()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def switch_frame(self, frame_class, *args):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, *args)
        if self._frame is not None:
            self._frame.destroy()
        self.rowconfigure([0,1,2], weight = 1)
        self.columnconfigure(0, weight = 1)
        self._frame = new_frame
        self._frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()

class StartPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)


        # configure grid layout (2x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with UI and appearance settings
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=30)
        self.sidebar_frame.grid(row=0, column=0, rowspan = 7, sticky="nsew", padx = 15, pady = 15)
        self.sidebar_frame.grid_rowconfigure(7, weight = 1)
        self.date_input_frame = customtkinter.CTkFrame(self, width=400, corner_radius=30)
        self.date_input_frame.grid(row = 0, column = 1, rowspan = 3, sticky = "nsew", padx = 15, pady = 15)
        self.date_input_frame.grid_rowconfigure(3, weight = 1)
        self.delete_input_frame = customtkinter.CTkFrame(self, width=200, corner_radius=30)
        self.delete_input_frame.grid(row = 0, column = 2, rowspan = 3, sticky = "nsew", padx = 15, pady = 15)
        self.delete_input_frame.grid_rowconfigure(3, weight = 1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Date Setup:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky = "ew")
        
        # Buttons above appearance mode section
        self.appearance_mode_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.quit)
        self.appearance_mode_button_1.grid(row=1, column=0, padx=20, pady=(50, 250))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w", font=("Arial", 16))
        self.appearance_mode_label.grid(row=3, column=0, padx=20, pady=(240, 5))
        
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event, font=("Arial", 16))
        self.appearance_mode_optionmenu.grid(row=4, column=0, padx=20, pady=(5, 5))
              
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w", font=("Arial", 16))
        self.scaling_label.grid(row=5, column=0, padx=20, pady=(5, 5))
        
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event, font=("Arial", 16))
        self.scaling_optionmenu.grid(row=6, column=0, padx=20, pady=(5, 20))
       

        # Example of adding a widget dynamically to the blank frame

        self.date_label = customtkinter.CTkLabel(self.date_input_frame, text="Please Enter Date in YYYYMMDD Format: ", font=("Arial", 40))
        self.date_label.grid(row=0, column=0, padx = 20, pady=(20,100), sticky="ew")
        
        self.date_entry = customtkinter.CTkEntry(self.date_input_frame, placeholder_text="YYYYMMDD", font=("Arial", 40))
        self.date_entry.grid(row=1, column=0, padx=20, pady=(10,100), sticky="ew")

        self.submit_button = customtkinter.CTkButton(self.date_input_frame, text="Submit", command=self.submit_date, font=("Arial", 40))
        self.submit_button.grid(row=2, column=0, padx=20, pady=(10, 100), sticky="ew")

        # Create and place selection menu above delete button
        self.selection_label = customtkinter.CTkLabel(self.delete_input_frame, text="Delete Options:", font=("Arial", 40))
        self.selection_label.grid(row=0, column=0, padx=20, pady=(20, 100), sticky="ew")

        self.selection_optionmenu = customtkinter.CTkOptionMenu(self.delete_input_frame, values=["Delete Year", "Delete Month", "Delete Date"], font=("Arial", 40))
        self.selection_optionmenu.grid(row=1, column=0, padx=20, pady=(10, 105), sticky="ew")

        self.delete_button = customtkinter.CTkButton(self.delete_input_frame, text="Delete", command=lambda: self.delete_date(self.selection_optionmenu.get(), self.date_entry.get()), font=("Arial", 40))
        self.delete_button.grid(row=2, column=0, padx=20, pady=(10, 100), sticky="ew")

        # set default values
        self.appearance_mode_optionmenu.set("System")
        self.scaling_optionmenu.set("100%")

    def submit_date(self):
        date = self.date_entry.get()
        if self.validate_date(date):
            # Assuming inputMode and StartPage are defined elsewhere
            self.expense, self.income = inputMode(date)
            self.master.switch_frame(EnterPage, self.expense, self.income, date)    
        else:
            tkinter.messagebox.showerror("Invalid Input", "Please enter a valid date in YYYYMMDD format.")

    def delete_date(self, entry, date):
        num = 0
        if(entry == "Delete Year"):
            num = 1
        elif(entry == "Delete Month"):
            num = 2
        elif(entry == "Delete Date"):
            num = 3
        else:
            tkinter.messagebox.showerror("Invalid Input", "Please Pick Deletion Selection")
        if self.validate_date(date):
            # Assuming inputMode and StartPage are defined elsewhere
            tkinter.messagebox.showinfo("Message Title" , delete(date, num))
        else:
            tkinter.messagebox.showerror("Invalid Input", "Please enter a valid date in YYYYMMDD format.")

    def validate_date(self, date_str):
        if len(date_str) == 8 and date_str.isdigit():
            year = int(date_str[:4])
            month = int(date_str[4:6])
            day = int(date_str[6:])
            if 1 <= month <= 12:
                days_in_month = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                if 1 <= day <= days_in_month[month - 1]:
                    return True
        return False
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

class EnterPage(customtkinter.CTkFrame):
    def __init__(self, master, expense,income, date):
        self.depositCounter = 0
        self.expenseCounter = 0
        self.expense2 = expense
        self.income2 = income
        customtkinter.CTkFrame.__init__(self, master)
        # configure grid layout (2x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with UI and appearance settings
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=30)
        self.sidebar_frame.grid(row=0, column=0, rowspan = 7, sticky="nsw", padx = 15, pady = 15)
        self.sidebar_frame.grid_rowconfigure(7, weight = 1)
        self.deposit_input_frame = customtkinter.CTkFrame(self, corner_radius=30)
        self.deposit_input_frame.grid(row = 0, column = 1, rowspan = 3, sticky = "nsew", padx = 15, pady = 15)
        self.deposit_input_frame.grid_rowconfigure(3, weight = 1)
        self.expense_input_frame = customtkinter.CTkFrame(self, corner_radius=30)
        self.expense_input_frame.grid(row = 0, column = 2, rowspan = 3, sticky = "nsew", padx = 15, pady = 15)
        self.expense_input_frame.grid_rowconfigure(3, weight = 1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Transaction Log:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky = "ew")
        
        # Buttons above appearance mode section
        self.appearance_mode_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.quit)
        self.appearance_mode_button_1.grid(row=1, column=0, padx=20, pady=(50, 5))

        self.appearance_mode_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Save Data", command=lambda: self.master.switch_frame(ResultPage, self.expense2, self.income2, date))
        self.appearance_mode_button_2.grid(row=2, column=0, padx=20, pady=(5, 240))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w", font=("Arial", 16))
        self.appearance_mode_label.grid(row=3, column=0, padx=20, pady=(240, 5))
        
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event, font=("Arial", 16))
        self.appearance_mode_optionmenu.grid(row=4, column=0, padx=20, pady=(5, 5))
              
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w", font=("Arial", 16))
        self.scaling_label.grid(row=5, column=0, padx=20, pady=(5, 5))
        
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event, font=("Arial", 16))
        self.scaling_optionmenu.grid(row=6, column=0, padx=20, pady=(5, 20))
        # Example of adding a widget dynamically to the blank frame
        self.expensesCategory = ["Housing", "Transportation", "Healthcare", "Education", "Entertainment and Leisure","Personal Care","Clothing","Insurance","Taxes","Miscellaneous"]
        self.depositCategory = ["Employment Income", "Self-Employment Income","Investment Income","Rental Income","Government Assistance","Other Income"]
        self.expenses_var = customtkinter.StringVar()
        self.deposit_var = customtkinter.StringVar()
        self.expenses_var.set(self.expensesCategory[0])
        self.deposit_var.set(self.depositCategory[0])
        self.deposit_label = customtkinter.CTkLabel(self.deposit_input_frame, text="Deposit:                             ", font=("Arial", 40))
        self.deposit_label.grid(row=0, column=0, padx = 50, pady=(20,50), sticky="ew")
        self.category_entry = customtkinter.CTkEntry(self.deposit_input_frame, placeholder_text="Sub-Category", font=("Arial", 40))
        self.category_entry.grid(row=1, column=0, padx=50, pady=(10,50), sticky="ew")
        self.value_entry = customtkinter.CTkEntry(self.deposit_input_frame, placeholder_text="0.00", font=("Arial", 40))
        self.value_entry.grid(row=2, column=0, padx=50, pady=(10,50), sticky="ew")
        
        self.deposit_entry = customtkinter.CTkOptionMenu(self.deposit_input_frame, values=self.depositCategory, font=("Arial", 40), variable = self.deposit_var)
        self.deposit_entry.grid(row=3, column=0, padx=50, pady=(10, 105), sticky="ew")

        self.submit_deposit_button = customtkinter.CTkButton(self.deposit_input_frame, text="Submit Deposit", command = lambda: self.submitDeposit(self.income2), font=("Arial", 40))
        self.submit_deposit_button.grid(row=4, column=0, padx=50, pady=(30, 100), sticky="ew")

        # Create and place selection menu above delete button
        self.withdraw_label = customtkinter.CTkLabel(self.expense_input_frame, text="Withdraw:                             ", font=("Arial", 40))
        self.withdraw_label.grid(row=0, column=0, padx=50, pady=(20, 50), sticky="ew")

        self.category_entry2 = customtkinter.CTkEntry(self.expense_input_frame, placeholder_text="Sub-Category", font=("Arial", 40))
        self.category_entry2.grid(row=1, column=0, padx=50, pady=(10,50), sticky="ew")

        self.value_entry2 = customtkinter.CTkEntry(self.expense_input_frame, placeholder_text="0.00", font=("Arial", 40))
        self.value_entry2.grid(row=2, column=0, padx=50, pady=(10,50), sticky="ew")

        self.expense_entry = customtkinter.CTkOptionMenu(self.expense_input_frame, values=self.expensesCategory, font=("Arial", 40), variable = self.expenses_var)
        self.expense_entry.grid(row=3, column=0, padx=50, pady=(10, 105), sticky="ew")

        self.submit_expense_button = customtkinter.CTkButton(self.expense_input_frame, text="Submit Expense", command = lambda:self.submitExpense(self.expense2),  font=("Arial", 40))
        self.submit_expense_button.grid(row=4, column=0, padx=50, pady=(30, 100), sticky="ew")


        # set default values
        self.appearance_mode_optionmenu.set("System")
        self.scaling_optionmenu.set("100%")
    def submitDeposit(self, income):
        source = self.category_entry.get()
        value = self.value_entry.get()
        depositDict = {"Employment Income":0, "Self-Employment Income":1,"Investment Income":2,"Rental Income":3,"Government Assistance":4,"Other Income":5}
        category = depositDict.get(self.deposit_var.get())
        if not is_alphabet(source):
            tkinter.messagebox.showerror("Invalid Input", "Please enter a valid source only letters and spaces allowed")
        elif not is_float(value):
            tkinter.messagebox.showerror("Invalid Input", "Please enter a valid amount of money")
        else:
                self.income = deposit(income, category, source, value)
                self.depositCounter+=1
                self.value_entry.delete(0, tkinter.END)
                self.category_entry.delete(0, tkinter.END)
                tkinter.messagebox.showerror("Message title", f'Deposits Submited: {self.depositCounter}')

    def submitExpense(self, expense):
        source = self.category_entry2.get()
        value = self.value_entry2.get()
        expensesDict = {"Housing": 0, "Transportation": 1, "Healthcare": 2, "Education": 3, "Entertainment and Leisure": 4,"Personal Care": 5,"Clothing":6,"Insurance":7,"Taxes":8,"Miscellaneous":9}
        category = expensesDict.get(self.expenses_var.get())
        if not is_alphabet(source):
            tkinter.messagebox.showerror("Invalid Input", "Please enter a valid source only letters and spaces allowed")
        elif not is_float(value):
            tkinter.messagebox.showerror("Invalid Input", "Please enter a valid amount of money")
        else:
            self.expense2 = withdraw(expense, category, source, value)
            self.expenseCounter+=1
            self.value_entry2.delete(0, tkinter.END)
            self.category_entry2.delete(0, tkinter.END)
            tkinter.messagebox.showerror("Message title", f'Withdraws Submited: {self.expenseCounter}')
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
class ResultPage(customtkinter.CTkFrame):
    def __init__(self, master, expense3, income3, date):
        saveData(expense3, income3, date)
        customtkinter.CTkFrame.__init__(self, master)
        # configure grid layout (2x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with UI and appearance settings
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=30)
        self.sidebar_frame.grid(row=0, column=0, rowspan = 7, sticky="nsw", padx = 15, pady = 15)
        self.sidebar_frame.grid_rowconfigure(7, weight = 1)
        self.deposit_input_frame = customtkinter.CTkFrame(self, corner_radius=30)
        self.deposit_input_frame.grid(row = 0, column = 1, rowspan = 3, sticky = "nsew", padx = 15, pady = 15)
        self.deposit_input_frame.grid_rowconfigure(17, weight = 1)
        self.deposit_input_frame.grid_columnconfigure(3, weight = 1)
        self.expense_input_frame = customtkinter.CTkFrame(self, corner_radius=30)
        self.expense_input_frame.grid(row = 0, column = 2, rowspan = 3, sticky = "nsew", padx = 15, pady = 15)
        self.expense_input_frame.grid_rowconfigure(3, weight = 1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Financial Overview:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky = "ew")
        
        # Buttons above appearance mode section
        self.appearance_mode_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.quit)
        self.appearance_mode_button_1.grid(row=1, column=0, padx=20, pady=(50, 10))

        self.appearance_mode_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Add Another Date", command=lambda: self.master.switch_frame(StartPage))
        self.appearance_mode_button_1.grid(row=2, column=0, padx=20, pady=(10, 250))

        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w", font=("Arial", 16))
        self.appearance_mode_label.grid(row=3, column=0, padx=20, pady=(240, 5))
        
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event, font=("Arial", 16))
        self.appearance_mode_optionmenu.grid(row=4, column=0, padx=20, pady=(5, 5))
              
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w", font=("Arial", 16))
        self.scaling_label.grid(row=5, column=0, padx=20, pady=(5, 5))
        
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event, font=("Arial", 16))
        self.scaling_optionmenu.grid(row=6, column=0, padx=20, pady=(5, 20))
       

        # Example of adding a widget dynamically to the blank frame
        self.deposit_label = customtkinter.CTkLabel(self.deposit_input_frame, text="Today's Categories:                  ", font=("Arial", 40))
        self.deposit_label.grid(row=0, column=0, padx = 50, pady=(20,50), sticky="ew")
        
        self.expensesCategory = ["Housing", "Transportation", "Healthcare", "Education", "Entertainment and Leisure","Personal Care","Clothing","Insurance","Taxes","Miscellaneous"]
        self.depositCategory = ["Employment Income", "Self-Employment Income","Investment Income","Rental Income","Government Assistance","Other Income"]
        for i, category in enumerate(self.expensesCategory):
            button = customtkinter.CTkButton(self.deposit_input_frame, command=lambda num=i: showDataDay(expense3, income3, date, num, None, None, 2), text=category, font=("Arial",20))
            button.grid(row=i+1, column=0, padx=20, pady=5)
        for j, cat in enumerate(self.depositCategory):
            button = customtkinter.CTkButton(self.deposit_input_frame,  command=lambda pum=j: showDataDay(expense3, income3, date, pum, None, None, 1), text=cat, font=("Arial",20))
            button.grid(row=j+11, column=0, padx=20, pady=5)

        # Create and place selection menu above delete button
        self.withdraw_label = customtkinter.CTkLabel(self.expense_input_frame, text="Overview:                             ", font=("Arial", 40))
        self.withdraw_label.grid(row=0, column=0, padx=50, pady=(20, 50), sticky="ew")

        self.delete_button = customtkinter.CTkButton(self.expense_input_frame, text="Day Results", command= lambda: showDataDay(expense3, income3, date), font=("Arial", 30))
        self.delete_button.grid(row=1, column=0, padx=50, pady=(30, 100), sticky="ew")

        self.delete_button = customtkinter.CTkButton(self.expense_input_frame, text="Month Results", command=lambda: showDataMonth(date), font=("Arial", 30))
        self.delete_button.grid(row=2, column=0, padx=50, pady=(30, 100), sticky="ew")

        self.delete_button = customtkinter.CTkButton(self.expense_input_frame, text="Year Results", command=lambda: showDataYear(date), font=("Arial", 30))
        self.delete_button.grid(row=3, column=0, padx=50, pady=(30, 100), sticky="ew")


        # set default values
        self.appearance_mode_optionmenu.set("System")
        self.scaling_optionmenu.set("100%")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = SampleApp()
    app.update_idletasks()
    app.mainloop()
