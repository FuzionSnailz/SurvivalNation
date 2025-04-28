from business import *
from data_domain import *

def display_bomb_details(serial_number, batteries, ports, indicators):
    print(f"Serial Number: {serial_number}")
    print(f"Batteries: {', '.join(batteries) if batteries else 'None'}")
    print(f"Ports: {', '.join(ports) if ports else 'None'}")
    print(f"Indicators: {', '.join(indicators) if indicators else 'None'}")

def get_user_input(prompt, valid_range=None):
    while True:
        try:
            user_input = int(input(prompt))
            if valid_range and user_input not in valid_range:
                raise ValueError("Input out of range.")
            return user_input
        except ValueError as e:
            print(f"Invalid input: {e}")

def defuse_bomb():
    import random
    data = DataAccess()
    bomb = BombDefusal(data)
    serial_number = data.serial_number
    serial_number_last_digit = int(serial_number[-1])
    ports = data.ports
    batteries = data.batteries
    num_batteries = len(batteries)
    indicators = data.indicators
    display_bomb_details(serial_number, batteries, ports, indicators)
    module_options = ["Wire Module", "Button Module", "Morse Code Module"]
    selected_modules = [random.choice(module_options) for _ in range(3)]
    print("\nModules to defuse:", ', '.join(selected_modules))
    strikes = 0
    completed_modules = [False, False, False]

    while not all(completed_modules):
        print("\nChoose a module to defuse:")
        for i, (module, completed) in enumerate(zip(selected_modules, completed_modules), start=1):
            if not completed:
                print(f"{i}: {module}")
        try:
            choice = int(input("Enter the number of the module you want to defuse: ")) - 1
            if choice < 0 or choice >= len(selected_modules) or completed_modules[choice]:
                raise ValueError("Invalid choice or module already completed.")
        except ValueError:
            print("Invalid input. Please enter a valid module number.")
            continue
        chosen_module = selected_modules[choice]
        if chosen_module == "Wire Module":
            wire_colors = data.wires
            wire_game_result, strikes = bomb.defuse_wire_module(
                wire_colors, serial_number_last_digit, strikes
            )
            if wire_game_result:
                print("\nCongratulations! You've completed the Wire module.")
                completed_modules[choice] = True
            else:
                print("\nYou failed the Wire module.")
        elif chosen_module == "Button Module":
            colored_button_label, button_label, indicators = data.button
            button_game_result, strikes = bomb.defuse_button_module(
                colored_button_label, button_label, num_batteries, indicators, strikes
            )
            if button_game_result:
                print("\nCongratulations! You've completed the Button module.")
                completed_modules[choice] = True
            else:
                print("\nYou failed the Button module.")
        elif chosen_module == "Morse Code Module":
            morse_code_result, strikes = bomb.defuse_morse_code_module(strikes)
            if morse_code_result:
                print("\nCongratulations! You've completed the Morse Code module.")
                completed_modules[choice] = True
            else:
                print("\nYou failed the Morse Code module.")
        else:
            print("Unexpected error. Please try again.")
    print("\nCongratulations! You've completed all modules and defused the bomb!")
