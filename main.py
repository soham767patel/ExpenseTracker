import matplotlib.pyplot as plt
import numpy as np
import csv
#each individual category is give by this it will have a catalog, a name, and a total cost
class Category:
    def __init__(self, name):
        self.name = name
        self.catalog = {}
        self.total = 0   
    def addition(self):
        self.total = sum(self.catalog.values())
def is_float(string):
    if string.replace(".","").isnumeric():
        return True
    else:
        return False
#This function will present the data in a nice manner preferably a graph or chart of sorts
def showData(amountDict, depositDict):
    while True:
        print("\nWould you like to see a specific Category or Overiew?\n1.Category\n2.Overview\n")
        represenation = input("\nType 1 or 2\n")
        if not(int(represenation) == 1 or int(represenation) == 2):
            print("Please Enter 1 or 2")
            continue
        break
    if int(represenation) == 2:
        expenseNum = []
        expenseLabel = []
        depositNum = []
        depositLabel = []
        for i in amountDict:
            i.addition()
            expenseNum.append(i.total)
            expenseLabel.append(i.name)
        for j in depositDict:
            j.addition()
            depositNum.append(j.total)
            depositLabel.append(j.name)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
        totalExpense = sum(expenseNum)
        totalDeposit = sum(depositNum)
        for i in range(len(depositNum)):
            depositLabel[i] = f"{depositLabel[i]}: {depositNum[i]/totalDeposit *100:.1f}%"
        for j in range(len(expenseNum)):
            expenseLabel[j] = f"{expenseLabel[j]}: {expenseNum[j]/totalExpense *100:.1f}%"
        # Plotting the pie chart for expenses
        ax1.pie(expenseNum, startangle=140)
        ax1.set_title(f'Expenses: ${totalExpense}')
        ax1.legend(expenseLabel, loc="best")

        # Plotting the pie chart for deposits
        ax2.pie(depositNum, startangle=140)
        ax2.set_title(f'Income: ${totalDeposit}')
        ax2.legend(depositLabel, title="Income", loc="best")
        plt.tight_layout()
        plt.show()
    elif int(represenation) == 1:
        label = []
        numbers = []
        index = 0
        total = 0
        while True:
            print("\nWould you like to see:\n")
            section = input("\n1.Deposit\n2.Expense\nType the corresponding number 1 or 2\n")
            if not int(section) == 1 and not int(section) == 2:
                print("Please enter a number")
                continue
            break
        if int(section) == 2:
            currentSec = amountDict
            print("\nHere are the Expenses Categories\n")
        elif int(section) == 1:
            currentSec = depositDict
            print("\nHere are the Deposit Categories\n")
        while True:
            for index, item in enumerate(currentSec):
                print(f'{index}. {item.name}')
            category = input("\nPlease enter the number corresponding to the category\n")
            if(not is_float(category) or int(category) >= len(amountDict)):
                print("Please enter a number")
                continue
            currentCatalog = currentSec[int(category)].catalog
            currentSec[int(category)].addition()
            total = currentSec[int(category)].total
            index = int(category)
            if total == 0:
                print("Sorry this category has no data, Please select another one")
                continue
            label = list(currentCatalog.keys())
            numbers = list(currentCatalog.values())
            break
        for i in range(len(numbers)):
            label[i] = f"{label[i]}: {numbers[i]/total *100:.1f}%"
        # Plotting the pie chart for expenses
        fig, (ax1) = plt.subplots(figsize=(14, 7))
        ax1.pie(numbers, startangle=140)
        ax1.set_title(f'{currentSec[index].name}: ${total}')
        ax1.legend(label, loc="best")

        plt.tight_layout()
        plt.show()
            
def saveData(amountDict, depositDict):
    print("\nSaving Data . . . ")
    
    # Prepare labels
    headersAmount = []
    headersDeposit = []
    itemsList = []
    maxLengthDep = 0
    maxLengthExp = 0
    for i, item in enumerate(amountDict):
        itemsList.append(list(item.catalog.keys()))
        itemsList.append(list(item.catalog.values()))
        maxLengthExp = max(maxLengthExp, len(item.catalog))
        headersAmount.append([f'{item.name}: Key'])
        headersAmount.append([f'{item.name}: Num'])
    for j, jtem in enumerate(depositDict):
        itemsList.append(list(jtem.catalog.keys()))
        itemsList.append(list(jtem.catalog.values()))
        maxLengthDep = max(maxLengthDep, len(item.catalog))
        headersDeposit.append([f'{jtem.name}: Key'])
        headersDeposit.append([f'{jtem.name}: Num'])
    # Write labels to CSV file
    with open('day_one_expense.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headersAmount)
        for i in range(maxLengthExp):
            row = []
            for j in range(10):
                if len(amountDict[j].catalog) > i:
                    row.append(list(amountDict[j].catalog.keys())[i])
                    row.append(list(amountDict[j].catalog.values())[i])
                else:
                    row.append("NaNa")
                    row.append(0)
            writer.writerow(row)
    with open('day_one_deposit.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headersDeposit)
        for i in range(maxLengthDep):
            row = []
            for j in range(6):
                if len(depositDict[j].catalog) > i:
                    row.append(list(depositDict[j].catalog.keys())[i])
                    row.append(list(depositDict[j].catalog.values())[i])
                else:
                    row.append("NaNa")
                    row.append(0)
            writer.writerow(row)
#This function will collect the expense
def withdraw(amountDict):
    while True:
        print("\nExpenses Categories:\n")
        for index, item in enumerate(amountDict):
            print(f'{index}. {item.name}')
        category = input("\nPlease enter the number corresponding to the category\n")
        if(not is_float(category) or int(category) >= len(amountDict)):
            print("Please enter a number")
            continue
        amount = input("How much did it cost? \nAmount: ")
        reason = input("What was it? \nWhat: ")
        if(reason.isalpha() and is_float(amount)):
            if(amountDict[int(category)].catalog.get(str(reason.lower())) == None):
                amountDict[int(category)].catalog[str(reason.lower())] = float(amount)
            else:
                newAmount = amountDict[int(category)].catalog.get(str(reason.lower())) + float(amount)
                amountDict[int(category)].catalog[str(reason.lower())] = float(newAmount)
            break
        else:
            print("Please make sure the What is all alphabets and Amount is only number")
            continue
    return amountDict
#This function will remove an expense
def deposit(depositDict):
    while True:
        print("\nDeposit Categories:\n")
        for index, item in enumerate(depositDict):
            print(f'{index}. {item.name}')
        category = input("\nPlease enter the number corresponding to the category\n")
        if(not is_float(category) or int(category) >= len(depositDict)):
            print("Please enter a number")
            continue
        amount = input("\nHow much did you add to the account?\nAmount: ")
        reason = input("\nWho is providing this deposit?\nSource: ")
        if(reason.isalpha() and is_float(amount)):
            if(depositDict[int(category)].catalog.get(str(reason.lower())) == None):
                depositDict[int(category)].catalog[str(reason.lower())] = float(amount)
            else:
                newAmount = depositDict[int(category)].catalog.get(str(reason.lower())) + float(amount)
                depositDict[int(category)].catalog[str(reason.lower())] = float(newAmount)
            break
        else:
            print("Please make sure the Source is all alphabets and Amount is only a number")
            continue
    return depositDict
def main():
    expensesCategory = ["Housing", "Transportation", "Healthcare", "Education", "Entertainment and Leisure","Personal Care","Clothing","Insurance","Taxes","Miscellaneous"]
    depositCategory = ["Employment Income", "Self-Employment Income","Investment Income","Rental Income","Government Assistance","Other Income"]
    expenseDict = []
    depositDict = []
    for i in expensesCategory:
        expenseDict.append(Category(i))
    for j in depositCategory:
        depositDict.append(Category(j))
    while True:
        #loop for making sure that we get correct response
        while True:
            choice = input("\nWould you like to make a deposit?: Y or N\n")
            if(choice == 'Y' or choice == 'N'):
                break
            else:
                print("Please only type Y or N")
        if(choice == "Y"):
            depositDict = deposit(depositDict)
        #loop for making sure that we get correct response
        choice = 'SAD'
        while True:
            choice = input("\nWould you like to add a expense?: Y or N\n")
            if(choice == 'Y' or choice == 'N'):
                break
            else:
                print("Please only type Y or N")
        if(choice == 'Y'):
            expenseDict = withdraw(expenseDict)
        choice = 'SAD'
        while True:
            choice = input("\nAre you all done?: Y or N\n")
            if(choice == 'Y' or choice == 'N'):
                break
            else:
                print("Please only type Y or N")
        if(choice == 'Y'):
            break
    saveData(expenseDict, depositDict)
    showData(expenseDict, depositDict)
main()