while True:
    # User input
    inches = input("How far would you like to fly (inches)? ")

    # Convert it to centimeter
    cm = float(inches) * 2.54

    # Check distance 
    if cm >= 20 and cm <= 500:
        print("Command accepted. Flying "+str(cm)+"cm")
    else:
        print("Command out of range.")
