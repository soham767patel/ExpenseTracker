#This function will present the data in a nice manner preferably a graph or chart of sorts
def showData(amountList, depositList):
    for i in amountList, depositList:
        name = i[0]
        amount = i[1]
        print(f'{name} cost you ${amount}')

#This function will collect the expense
def withdraw(amountList):
    amount = input("How much did it cost? \n")
    nameAmount = input("What was it? \n")
    amountList.append((nameAmount , amount))
    return amountList
#This function will remove an expense
def deposit(depositList):
    amount = input("How much did you add to the account?\n")
    reason = input("Why did you deposit?\n")
    depositList.append((reason, amount))
    return depositList
def main():
    expenseList = []
    depositList = []
    while True:
        choice = input("Would you like to make a deposit?: Y or N\n")
        while(choice == 'Y'):
            deposit(depositList)
            choice = input("Would you like to make a deposit?: Y or N\n")
        choice = input("Would you like to add an expense?: Y or N\n")
        while(choice == 'Y'):
            expenseList = withdraw(expenseList)
            choice = input("Would you like to add an expense?: Y or N\n")
        choice = input("Are you all done?: Y or N\n")
        if(choice == 'Y'):
            break
    showData(expenseList, depositList)
main()