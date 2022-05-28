# Calc.py
# Xtreme Calculator
# Anthony


def menu():
    print("="*30)
    print("Xtreme Calculator")
    print("by Anthony")
    print("="*30)
    print("="*30)
    print("[1] Add")
    print("[2] Subtract")
    print("[3] Multiply")
    print("[4] Divide")
    print("[q] Exit")

option = ""
while option!="q":
    menu()
    option = input("Please, select an option: ")
    # print('the selected option is ' + option)

    #ask for the 1st number
    num1 = float(input('Enter the first number: '))
    #ask for the  2nd number
    num2 = float(input('Enter the second number: '))

    print(f"DEBUG: num1:{num1} num2:{num2}")

    result = 0

    if option=="1":
        result = num1+num2
        print(f"The result is: {result}")

    elif option=="2":
        result = num1-num2
        print(f"The result is: {result}")

    elif option=="3":
        result = num1 * num2
        print(f"The result is: {result}")

    elif option=="4":
        if num2 != 0:
            result = num1 / num2
            print(f"The result is: {result}")
        else:
            print("Cannot divide by zero :(")
    input('Press enter to continue...')
