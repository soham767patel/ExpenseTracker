#This function will present the data in a nice manner preferably a graph or chart of sorts
def showData(amountList):
    print(amountList)

#This function will collect the expense
def withdraw(amountList):
    amount = input("How much did it cost?")
    nameAmount = input("What was it?")
    return amountList.append({nameAmount : amount})
#This function will remove an expense
def deposit():
    input("How much did you add to the account?")

def main():
    while True:
        withdraw()
        deposit()
        showData()
main()