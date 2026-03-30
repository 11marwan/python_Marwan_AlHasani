def convert(): 
    # Prompt for Input
    user_input = input("Enter a number: ")
    try:
        # Try to convert input to integer
        number = int(user_input)
        # Success Message
        print(f"You entered the number: {number}")
    except ValueError:
        # Handle ValueError
        print("Error: That is not a valid number.")