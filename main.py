import matplotlib.pyplot as plt
import numpy as np
#each individual category is give by this it will have a catalog, a name, and a total cost
class Category:
    def __init__(self, name):
        self.name = name
        self.catalog = {}
        self.total = 0   
def is_float(string):
    if string.replace(".","").isnumeric():
        return True
    else:
        return False
#This function will present the data in a nice manner preferably a graph or chart of sorts
def showData(amountDict, depositDict):
    expenseLabel, expenseNum = zip(*amountDict.items())
    depositLabel, depositNum = zip(*depositDict.items())
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(10,10))
    ax1.pie(expenseNum, labels = expenseLabel)
    ax1.set_title('Expenses')
    ax2.pie(depositNum, labels = depositLabel)
    ax2.set_title('Income')
    plt.show()

#This function will collect the expense
def withdraw(amountDict):
    while True:
        print("\nDeposit Categories:\n")
        for index, item in enumerate(amountDict):
            print(f'{index}. {item.name}')
        category = input("\nPlease enter the number corresponding to the category\n")
        if(not is_float(category) or int(category) >= len(amountDict)):
            print("Please enter a number")
            continue
        amount = input("How much did it cost? \nAmount: ")
        reason = input("What was it? \nWhat: ")
        if(reason.isalpha() and is_float(amount)):
            if(amountDict.get(str(reason.lower())) == None):
                amountDict[str(reason.lower())] = float(amount)
            else:
                newAmount = amountDict.get(str(reason.lower())) + float(amount)
                amountDict[str(reason.lower())] = float(newAmount)
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
    showData(expenseDict, depositDict)
main()