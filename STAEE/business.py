from data_domain import *
import sys


class BombDefusal:

    def __init__(self, data):
        self.data = data
        self.wire_module_completed = False
        self.button_module_completed = False
        self.morse_code_module_completed = False

    @staticmethod
    def defuse_wire_module(wire_colors, serial_number_last_digit, strikes):
        print(f"\nTotal Strikes: {strikes}")
        display_colored_wires(wire_colors)
        while strikes < 3:
            try:
                player_input = int(input("Guess which wire to cut (enter the position): "))
                if 1 <= player_input <= len(wire_colors):
                    wire_position = choose_wire_to_cut(wire_colors, serial_number_last_digit)
                    chosen_wire_color = wire_colors[player_input - 1]
                    print(
                        f"Chosen Wire to Cut: {player_input} ({lit.__dict__[chosen_wire_color.upper()]}{lit.__dict__[chosen_wire_color.upper()]}{'wire'.title()}{lit.ENDC})")

                    if wire_position == player_input:
                        return True, strikes
                    else:
                        print(f"Oops! You chose to cut wire {player_input}.")
                        strikes += 1
                        print(f"You now have {strikes} strike(s).")
                else:
                    print(f"Invalid wire position. Please enter a number between 1 and {len(wire_colors)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        display_result_and_exit(False, "Wire")
        return False, strikes

    @staticmethod
    def defuse_button_module(colored_button_label, button_label, num_batteries, indicators, strikes):
        print(f"\nTotal Strikes: {strikes}")
        print(f"\nButton: {colored_button_label}")
        while strikes < 3:
            player_input = input("Enter 'hold' or 'press': ").lower()
            result = press_or_hold_button(colored_button_label, button_label, num_batteries, indicators)
            if player_input == result:
                if player_input == 'press':
                    return True, strikes
                elif player_input == 'hold':
                    print(f"\nYou chose to hold the button.")
                    strip_result, strikes = strip_color_game(strikes)
                    if strip_result:
                        return True, strikes
                    else:
                        print("Incorrect input. Please try again.")
            else:
                print("Incorrect input. Please try again.")
                strikes += 1
                print(f"You now have {strikes} strike(s).")
        display_result_and_exit(False, "Button")
        return False, strikes

    @staticmethod
    def defuse_morse_code_module(strikes):
        morse_code, chosen_word = generate_morse_code()
        print(f"\nTotal Strikes: {strikes}")
        print(f"\nMorse Code: {morse_code}")
        while strikes < 3:
            try:
                player_input = float(input("Enter the frequency: "))
                correct_frequency = morse_freq(chosen_word)
                if player_input == correct_frequency:
                    print("Correct! Module defused.")
                    return True, strikes
                else:
                    print("Oops! Try again.")
                    strikes += 1
                    print(f"You now have {strikes} strike(s).")
            except ValueError:
                print("Invalid input. Please enter a valid frequency.")
        display_result_and_exit(False, "Morse Code")
        return False, strikes

def choose_wire_to_cut(wire_colors, serial_number_last_digit):
    num_wires = len(wire_colors)
    if num_wires == 3:
        if 'red' not in wire_colors:
            return 2
        elif wire_colors[-1] == 'white':
            return num_wires
        elif wire_colors.count('blue') > 1:
            return num_wires - wire_colors[::-1].index('blue')
    elif num_wires == 4:
        if wire_colors.count('red') > 1 and serial_number_last_digit % 2 != 0:
            return num_wires - wire_colors[::-1].index('red')
        elif wire_colors[-1] == 'yellow' and 'red' not in wire_colors:
            return 1
        elif wire_colors.count('blue') == 1:
            return 1
        elif wire_colors.count('yellow') > 1:
            return num_wires
        else:
            return 2
    elif num_wires == 5:
        if wire_colors[-1] == 'black' and serial_number_last_digit % 2 != 0:
            return 4
        elif wire_colors.count('red') == 1 and wire_colors.count('yellow') > 1:
            return 1
        elif 'black' not in wire_colors:
            return 2
        else:
            return 1
        pass
    elif num_wires == 6:
        if 'yellow' not in wire_colors and serial_number_last_digit % 2 != 0:
            return 3
        elif wire_colors.count('yellow') == 1 and wire_colors.count('white') > 1:
            return 4
        elif 'red' not in wire_colors:
            return num_wires
        else:
            return 4
        pass
    return num_wires

def morse_freq(chosen_word):
    word_to_frequency = {
        'shell': 3.505,
        'halls': 3.515,
        'slick': 3.522,
        'trick': 3.532,
        'boxes': 3.535,
        'leaks': 3.542,
        'strobe': 3.545,
        'bistro': 3.552,
        'flick': 3.555,
        'bombs': 3.565,
        'break': 3.572,
        'brick': 3.575,
        'steak': 3.582,
        'sting': 3.592,
        'vector': 3.595,
        'beats': 3.600

    }

    return word_to_frequency.get(chosen_word, None)

def display_colored_wires(wire_colors):
    print("\nWire Colors:")
    for i, color in enumerate(wire_colors, start=1):
        colored_wire = getattr(lit, color.upper()) + 'wire' + lit.ENDC
        print(f"{i}: {colored_wire}")

def display_result_and_exit(success, module_name):
    if success:
        print(f"\nCongratulations! You've completed the {module_name} module.")
    else:
        print(f"\nYou failed the {module_name} module.")
        print("BOOM! EVERYONE DIED ALL BECAUSE OF YOU. YOU HAD ONE JOB!!!")
        sys.exit()

def generate_morse_code():
    morse_code_lists = {
        'shell': ['...', '....', '.', '.-..', '.-..'],
        'halls': ['....', '.-', '.-..', '.-..', '...'],
        'slick': ['...', '.-..', '..', '-.-.', '-.-'],
        'trick': ['-', '.-.', '..', '-.-.', '-.-'],
        'boxes': ['-...', '---', '-..-', '.', '...'],
        'leaks': ['.-..', '.', '.-', '-.-', '...'],
        'strobe': ['...', '-', '.-.', '---', '-...', '.'],
        'bistro': ['-...', '..', '...', '-', '.-.', '---'],
        'flick': ['..-.', '.-..', '..', '-.-.', '-.-'],
        'bombs': ['-...', '---', '--', '-...', '...'],
        'break': ['-...', '.-.', '.', '.-', '-.-'],
        'brick': ['-...', '.-.', '..', '-.-.', '-.-'],
        'steak': ['...', '-', '.', '.-', '-.-'],
        'sting': ['...', '-', '..', '-.', '--.'],
        'vector': ['...-', '.', '-.-.', '-', '---', '.-.'],
        'beats': ['-...', '.', '.-', '-', '...']
    }
    chosen_morse = random.choice(list(morse_code_lists.keys()))
    morse_code = ' '.join(morse_code_lists[chosen_morse])
    return morse_code, chosen_morse


def press_or_hold_button(colored_button_label, button_label, num_batteries, indicators):
    lit_indicators_red = [indicator.replace(lit.RED, '') for indicator in indicators]

    if colored_button_label == lit.BLUE and button_label == 'abort':
        return 'hold'
    elif num_batteries > 1 and button_label == 'detonate':
        return 'press'
    elif colored_button_label == lit.WHITE and 'CAR' in lit_indicators_red:
        return 'hold'
    elif num_batteries > 2 and "FRK" in lit_indicators_red:
        return 'press'
    elif colored_button_label == lit.YELLOW:
        return 'hold'
    elif colored_button_label == lit.RED and button_label == 'hold':
        return 'press'
    else:
        return 'hold'

def strip_numb(color_strip):
    if color_strip == lit.BLUE:
        return 4
    elif color_strip == lit.WHITE:
        return 1
    elif color_strip == lit.YELLOW:
        return 5
    else:
        return 1

def strip_color_game(strikes):
    while strikes < 3:
        color_strip = lit.random_color()
        colored_strip = f"{color_strip}strip{lit.ENDC}"
        print(f"\nTotal Strikes: {strikes}")
        print(f"\nColored Strip: {colored_strip}")
        try:
            player_input = input("Enter a number to defuse the strip: ")
            if player_input.isdigit():
                if int(player_input) == strip_numb(color_strip):
                    return True, strikes
                else:
                    print("Oops! Try again.")
                    strikes += 1
                    print(f"You now have {strikes} strike(s).")
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return False, strikes
