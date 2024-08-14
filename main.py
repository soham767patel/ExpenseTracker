import matplotlib.pyplot as plt
import numpy as np
def is_float(string):
    if string.replace(".","").isnumeric():
        return True
    else:
        return False
#This function will present the data in a nice manner preferably a graph or chart of sorts
def showData(amountDict, depositDict):
    expenseLabel, expenseNum = zip(*amountDict.items())
    depositLabel, depositNum = zip(*depositDict.items())


    plt.pie(expenseNum, labels = expenseLabel)
    plt.show()
    plt.pie(depositNum, labels = depositLabel)
    plt.show()

#This function will collect the expense
def withdraw(amountDict):
    while True:
        amount = input("How much did it cost? \nHow: ")
        reason = input("What was it? \nWhat: ")
        if(reason.isalpha() and is_float(amount)):
            if(amountDict.get(str(reason.lower())) == None):
                amountDict[str(reason.lower())] = float(amount)
            else:
                newAmount = amountDict.get(str(reason.lower())) + float(amount)
                amountDict[str(reason.lower())] = float(newAmount)
            break
        else:
            print("Please make sure the What is all alphabets and How is only number")
            continue
    return amountDict
#This function will remove an expense
def deposit(depositDict):
    while True:
        amount = input("How much did you add to the account?\nHow: ")
        reason = input("Who is providing this deposit?\nWho: ")
        if(reason.isalpha() and is_float(amount)):
            if(depositDict.get(str(reason.lower())) == None):
                depositDict[str(reason.lower())] = float(amount)
            else:
                newAmount = depositDict.get(str(reason.lower())) + float(amount)
                depositDict[str(reason.lower())] = float(newAmount)
            break
        else:
            print("Please make sure the Who is all alphabets and How is only number")
            continue
    return depositDict
def main():
    expenseDict = {}
    depositDict = {}
    while True:
        #loop for making sure that we get correct response
        while True:
            choice = input("Would you like to make a deposit?: Y or N\n")
            if(choice == 'Y' or choice == 'N'):
                break
            else:
                print("Please only type Y or N")
        if(choice == "Y"):
            depositDict = deposit(depositDict)
        #loop for making sure that we get correct response
        choice = 'SAD'
        while True:
            choice = input("Would you like to add a expense?: Y or N\n")
            if(choice == 'Y' or choice == 'N'):
                break
            else:
                print("Please only type Y or N")
        if(choice == 'Y'):
            expenseDict = withdraw(expenseDict)
        choice = 'SAD'
        while True:
            choice = input("Are you all done?: Y or N\n")
            if(choice == 'Y' or choice == 'N'):
                break
            else:
                print("Please only type Y or N")
        if(choice == 'Y'):
            break
    showData(expenseDict, depositDict)
main()