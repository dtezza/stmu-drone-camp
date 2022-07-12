# Function definition 
def sayHello():
    print("Hello!")
    print("This is a function example")
    print("End of function")
    
# Function definition (parameter)
def printRow(number):
    print(str(number)+" "+ str(number*2)+" "+ str(number*3)+" "+ str(number*4)+" "+ str(number*5))

# Call the function
print("Before function call")
sayHello()
print("After function call")

for i in range(10):
    printRow(i+1)

print("End of program")

