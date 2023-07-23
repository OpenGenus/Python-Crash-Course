#store previous compuation value
prev_value = 0

print('''\nInstructions \n1. To perform operations on multiple values, enter the numbers separated by space. Example to add: 4 5 6 
\n2. To use the previously calculated value, use the letter 'p'. \nExample: Add 5 to previously calculated value of 7530: p+5 = 7535\n 
\n3. To perform power operations, use the expression choice and use the symbol **\n''')
while(True):
    print("\n ......... \n Calculator\n .........\n")

    try:
        operation = int(input('''Choose the operation : 1/2/3/4/5/6 \n 1. Addition \n 2. Subtraction \n 3. Multiplication \n 4. Division \n 5. Enter expression \n 6. Exit \n Input: '''))
        if operation not in {1,2,3,4,5,6}:
            print("!!! Enter only numbers 1/2/3/4/5/6 !!!")
            continue
    except ValueError:
        print("!!! Enter only numbers 1/2/3/4/5/6 !!!")
        continue
    
    
    if operation not in {4, 5,6}:
        try:
            x = input("Enter values: ").split()

            for index in range(len(x)):
                if x[index] == 'p':
                    x[index] = prev_value
            num_list = [int(x) for x in x]

    
        except ValueError:
            print("Enter a number for valid input!\n")
            continue
    
    #addition
    if operation == 1:
        sum=0
         
        for item in num_list:
            sum += item
        print("Sum: ", sum)
        prev_value = sum
    
    #subtraction
    elif operation == 2:
        diff=0
         
        for item in num_list:
            diff += item
        print("Difference: ", diff)
        prev_value = diff

    #multiplication
    elif operation == 3:
        product=1
         
        for item in num_list:
            product *= item
        print("Product: ", product)
        prev_value = product

    #division
    elif operation == 4:
        num1 = input("Enter dividend: ")
        num2 = input("Enter divisor: ")

        if num1 == 'p':
            num1 = prev_value

        elif num2 == 'p':
            num2 = prev_value

        div = int(num1)/int(num2) 
        
        round_div = round(div, 5)
        print("Result: ", num1, "/", num2, "=", round_div)
        prev_value = round_div

    #expression 
    elif operation == 5:
        try:
            exp = input("Enter the expression \n")

            exp = list(exp)

            for letter in range(len(exp)):
                if exp[letter] == 'p':
                    exp[letter] = str(prev_value)
            exp = "".join(exp)

            result = eval(exp)
            print("Result: "+ exp + ' = ' + str(result))
            prev_value = result

        except SyntaxError:
            print("Enter a valid expression!\n")
            continue
    
    elif operation == 6:
        exit()











