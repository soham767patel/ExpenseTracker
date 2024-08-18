import matplotlib.pyplot as plt
import numpy as np
import csv
import os.path
#each individual category is give by this it will have a catalog, a name, and a total cost
class Category:
    def __init__(self, name):
        self.name = name
        self.catalog = {}
        self.total = 0   
    def addition(self):
        self.total = sum(self.catalog.values())
def is_float(string):
    if string.replace(".","").isnumeric() and not string.replace(".","").replace("0","") == "":
        return True
    else:
        return False
def is_alphabet(string):
    if string.replace(" ","").isalpha():
        return True
    else:
        return False
#This function will present the data in a nice manner preferably a graph or chart of sorts
def showDataDay(amountDict, depositDict, date, isItACategory = None, isMonth = None, isYear = None, deposit = 0):
    if isItACategory == None:
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
        if isMonth == None and isYear == None:
            fig.suptitle(f'Date: {date}', fontsize=30)
        elif isYear == None:
            monthDict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
            monthNum = date[4] + date[5]
            month = int(monthNum)
            fig.suptitle(f'{monthDict[month]} {date[:4]}', fontsize=30)
        else:
            fig.suptitle(f'{date[:4]}', fontsize=30)
        totalExpense = sum(expenseNum)
        totalDeposit = sum(depositNum)
        for i in range(len(depositNum)):
            depositLabel[i] = f"{depositLabel[i]}: {depositNum[i]/totalDeposit *100:.1f}%"
        for j in range(len(expenseNum)):
            expenseLabel[j] = f"{expenseLabel[j]}: {expenseNum[j]/totalExpense *100:.1f}%"
        # Plotting the pie chart for expenses
        ax1.pie(expenseNum, startangle=140)
        ax1.set_title(f'Expenses: ${totalExpense}')
        ax1.legend(expenseLabel,title="Expense", loc="best")

        # Plotting the pie chart for deposits
        ax2.pie(depositNum, startangle=140)
        ax2.set_title(f'Income: ${totalDeposit}')
        ax2.legend(depositLabel, title="Income", loc="best")
        plt.tight_layout()
        plt.show()
    #Category Print
    else:
        if deposit == 0:
            pass
        elif deposit == 1:
            currentSec = depositDict
        elif deposit == 2:
            currentSec = amountDict
        category = isItACategory
        label = []
        numbers = []
        total = 0
        currentCatalog = currentSec[int(category)].catalog
        currentSec[int(category)].addition()
        total = currentSec[int(category)].total
        index = int(category)
        label = list(currentCatalog.keys())
        numbers = list(currentCatalog.values())
        for i in range(len(numbers)):
            label[i] = f"{label[i]}: {numbers[i]/total *100:.1f}%"
        # Plotting the pie chart for expenses
        fig, (ax1) = plt.subplots(figsize=(14, 7))
        ax1.pie(numbers, startangle=140)
        ax1.set_title(f'{currentSec[index].name}: ${total}')
        ax1.legend(label, loc="best")

        plt.tight_layout()
        plt.show()      
def showDataMonth(currDate):
    expensesCategory = ["Housing", "Transportation", "Healthcare", "Education", "Entertainment and Leisure","Personal Care","Clothing","Insurance","Taxes","Miscellaneous"]
    depositCategory = ["Employment Income", "Self-Employment Income","Investment Income","Rental Income","Government Assistance","Other Income"]
    expenseDict = []
    depositDict = []
    for i in expensesCategory:
        expenseDict.append(Category(i))
    for j in depositCategory:
        depositDict.append(Category(j))
    currentDirectory = os.getcwd()
    for i in range(1, 32):
        if i < 10:
            date = currDate[:6] + "0" + str(i)
        else:
            date = currDate[:6] + str(i)
        currentPathExpense = currentDirectory + f'/{date}_expense.csv'
        currentPathDeposit = currentDirectory + f'/{date}_deposit.csv'
        if os.path.exists(currentPathDeposit):
            print(f'{date} deposit file exists . . . \n')
            file = f'{date}_deposit.csv'
            with open(file, 'r') as csvfile:
                next(csvfile)
                reader = csv.reader(csvfile)
                for row in reader:
                    for i in range(0, 12, 2):
                        if(row[i] == "NaNa"):
                            pass
                        else:
                            if depositDict[int(i/2)].catalog.get(row[i]) == None :
                                depositDict[int(i/2)].catalog[row[i]] = float(row[i+1])
                            else:
                                newAmount = depositDict[i/2].catalog.get(row[i]) + float(row[i+1])
                                depositDict[int(i/2)].catalog[row[i]] = float(newAmount)
                for k in range(0,6,1):
                    depositDict[int(k)].addition()
        else:
            print(f'{date} deposit file does not exist . . . not uploading . . . \n')
        if os.path.exists(currentPathExpense):
            print(f'{date} expense file exists . . .\n')
            file = f'{date}_expense.csv'
            with open(file, 'r') as csvfile:
                next(csvfile)
                reader = csv.reader(csvfile)
                for row in reader:
                    for i in range(0, 20, 2):
                        if(row[i] == "NaNa"):
                            pass
                        else:
                            if expenseDict[int(i/2)].catalog.get(row[i]) == None :
                                expenseDict[int(i/2)].catalog[row[i]] = float(row[i+1])
                            else:
                                newAmount = expenseDict[int(i/2)].catalog.get(row[i]) + float(row[i+1])
                                expenseDict[int(i/2)].catalog[row[i]] = float(newAmount) 
                for j in range(0,10,1):
                    expenseDict[int(j)].addition()
        else:
            print(f'{date} expense file does not exist . . . not uploading . . . \n')
    showDataDay(expenseDict, depositDict, currDate, None, 1)
def showDataYear(currDate):
    expensesCategory = ["Housing", "Transportation", "Healthcare", "Education", "Entertainment and Leisure","Personal Care","Clothing","Insurance","Taxes","Miscellaneous"]
    depositCategory = ["Employment Income", "Self-Employment Income","Investment Income","Rental Income","Government Assistance","Other Income"]
    expenseDict = []
    depositDict = []
    for i in expensesCategory:
        expenseDict.append(Category(i))
    for j in depositCategory:
        depositDict.append(Category(j))
    currentDirectory = os.getcwd()
    for i in range(1, 13):
        year = currDate
        if i < 10:
                currMon =  currDate[:4] + "0" + str(i)
        else:
                currMon = currDate[:4] + str(i)
        for i in range(1, 32):
            if i < 10:
                date =  currMon + "0" + str(i)
            else:
                date = currMon + str(i)
            currentPathExpense = currentDirectory + f'/{date}_expense.csv'
            currentPathDeposit = currentDirectory + f'/{date}_deposit.csv'
            if os.path.exists(currentPathDeposit):
                print(f'{date} deposit file exists . . . \n')
                file = f'{date}_deposit.csv'
                with open(file, 'r') as csvfile:
                    next(csvfile)
                    reader = csv.reader(csvfile)
                    for row in reader:
                        for i in range(0, 12, 2):
                            if(row[i] == "NaNa"):
                                pass
                            else:
                                if depositDict[int(i/2)].catalog.get(row[i]) == None :
                                    depositDict[int(i/2)].catalog[row[i]] = float(row[i+1])
                                else:
                                    newAmount = depositDict[i/2].catalog.get(row[i]) + float(row[i+1])
                                    depositDict[int(i/2)].catalog[row[i]] = float(newAmount)
                    for k in range(0,6,1):
                        depositDict[int(k)].addition()
            else:
                print(f'{date} deposit file does not exist . . . not uploading . . . \n')
            if os.path.exists(currentPathExpense):
                print(f'{date} expense file exists . . .\n')
                file = f'{date}_expense.csv'
                with open(file, 'r') as csvfile:
                    next(csvfile)
                    reader = csv.reader(csvfile)
                    for row in reader:
                        for i in range(0, 20, 2):
                            if(row[i] == "NaNa"):
                                pass
                            else:
                                if expenseDict[int(i/2)].catalog.get(row[i]) == None :
                                    expenseDict[int(i/2)].catalog[row[i]] = float(row[i+1])
                                else:
                                    newAmount = expenseDict[int(i/2)].catalog.get(row[i]) + float(row[i+1])
                                    expenseDict[int(i/2)].catalog[row[i]] = float(newAmount) 
                    for j in range(0,10,1):
                        expenseDict[int(j)].addition()
            else:
                print(f'{date} expense file does not exist . . . not uploading . . . \n')
    showDataDay(expenseDict, depositDict, currDate, None, 1, 1)

def saveData(amountDict, depositDict, currDate):
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
        maxLengthDep = max(maxLengthDep, len(jtem.catalog))
        headersDeposit.append([f'{jtem.name}: Key'])
        headersDeposit.append([f'{jtem.name}: Num'])
    # Write labels to CSV file
    with open(f'{currDate}_expense.csv', 'w', newline='') as csvfile:
        print("\nSaving Expense . . . ")
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
    with open(f'{currDate}_deposit.csv', 'w', newline='') as csvfile:
        print("\nSaving Deposit . . . ")
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
def inputMode(date):
    expensesCategory = ["Housing", "Transportation", "Healthcare", "Education", "Entertainment and Leisure","Personal Care","Clothing","Insurance","Taxes","Miscellaneous"]
    depositCategory = ["Employment Income", "Self-Employment Income","Investment Income","Rental Income","Government Assistance","Other Income"]
    expenseDict = []
    depositDict = []
    for i in expensesCategory:
        expenseDict.append(Category(i))
    for j in depositCategory:
        depositDict.append(Category(j))
    currentDirectory = os.getcwd()
    currentPathExpense = currentDirectory + f'/{date}_expense.csv'
    currentPathDeposit = currentDirectory + f'/{date}_deposit.csv'
    if os.path.exists(currentPathDeposit):
        print(f'{date} deposit file exists . . . \n')
        file = f'{date}_deposit.csv'
        with open(file, 'r') as csvfile:
            next(csvfile)
            reader = csv.reader(csvfile)
            for row in reader:
                for i in range(0, 12, 2):
                    if(row[i] == "NaNa"):
                        pass
                    else:
                        if depositDict[int(i/2)].catalog.get(row[i]) == None :
                            depositDict[int(i/2)].catalog[row[i]] = float(row[i+1])
                        else:
                            newAmount = depositDict[i/2].catalog.get(row[i]) + float(row[i+1])
                            depositDict[int(i/2)].catalog[row[i]] = float(newAmount)
            for k in range(0,6,1):
                depositDict[int(k)].addition()
    else:
        print(f'{date} deposit file does not exist . . . not uploading . . . \n')
    if os.path.exists(currentPathExpense):
        print(f'{date} expense file exists . . .\n')
        file = f'{date}_expense.csv'
        with open(file, 'r') as csvfile:
            next(csvfile)
            reader = csv.reader(csvfile)
            for row in reader:
                for i in range(0, 20, 2):
                    if(row[i] == "NaNa"):
                        pass
                    else:
                        if expenseDict[int(i/2)].catalog.get(row[i]) == None :
                            expenseDict[int(i/2)].catalog[row[i]] = float(row[i+1])
                        else:
                            newAmount = expenseDict[int(i/2)].catalog.get(row[i]) + float(row[i+1])
                            expenseDict[int(i/2)].catalog[row[i]] = float(newAmount) 
            for j in range(0,10,1):
                expenseDict[int(j)].addition()
    else:
        print(f'{date} expense file does not exist . . . not uploading . . . \n')
    return expenseDict, depositDict
def withdraw(amountDict, index, reason, amount):
    if(amountDict[int(index)].catalog.get(str(reason.lower())) == None):
        amountDict[int(index)].catalog[str(reason.lower())] = float(amount)
    else:
        newAmount = amountDict[int(index)].catalog.get(str(reason.lower())) + float(amount)
        amountDict[int(index)].catalog[str(reason.lower())] = float(newAmount)

    return amountDict
#This function will remove an expense
def deposit(depositDict, index, reason, amount):
    if(depositDict[int(index)].catalog.get(str(reason.lower())) == None):
        depositDict[int(index)].catalog[str(reason.lower())] = float(amount)
    else:
        newAmount = depositDict[int(index)].catalog.get(str(reason.lower())) + float(amount)
        depositDict[int(index)].catalog[str(reason.lower())] = float(newAmount)
    return depositDict
