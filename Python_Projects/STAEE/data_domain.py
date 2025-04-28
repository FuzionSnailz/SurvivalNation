import random
import string

class DataAccess:
    def __init__(self):
        self.serial_number = self.generate_serial_number()
        self.batteries, self.num_batteries = self.generate_batteries()
        self.ports = self.generate_ports()
        self.indicators = self.generate_indicators()
        self.wires = self.generate_wires()
        self.color_strip = self.generate_color_strip()
        self.button = self.generate_button_color_label(self.indicators)

    @staticmethod
    def generate_serial_number():
        serial_number = ''.join([
            random.choice(string.ascii_uppercase + string.digits), random.choice(string.ascii_uppercase + string.digits),
            random.choice(string.digits), random.choice(string.ascii_uppercase),
            random.choice(string.ascii_uppercase), random.choice(string.digits)
        ])
        return serial_number

    @staticmethod
    def generate_batteries():
        batteries = random.choices(["AA", "D"], k=random.randint(1, 5))
        return batteries, len(batteries)

    @staticmethod
    def generate_ports():
        ports = ['DVI', 'Parallel', 'PS2', 'RJ45', 'Serial', 'Sterio']
        return random.choices(ports, k=random.randint(0, 6))

    @staticmethod
    def generate_indicators():
        indicators = random.sample(['SND', 'CLR', 'CAR', 'IND', 'FRQ', 'SIG', 'NSA', 'MSA', 'TRN', 'BOB', 'FRK'], k=random.randint(0, 7))
        return [f'{lit.RED}{ind}{lit.ENDC}' if random.choice([True, False]) else ind for ind in indicators] if indicators else []

    @staticmethod
    def generate_wires():
        wire_colors = ['red', 'yellow', 'blue', 'black', 'white']
        return [random.choice(wire_colors) for _ in range(random.randint(3, 6))]

    @staticmethod
    def generate_color_strip():
        random_colors = [lit.RED, lit.YELLOW, lit.BLUE, lit.BLACK, lit.WHITE]
        return random.choice(random_colors)

    @staticmethod
    def generate_button_color_label(indicators):
        button_label = random.choice(['abort', 'detonate', 'hold', 'press'])
        colored_button_label = f'{lit.random_color()}{button_label}{lit.ENDC}'
        indicators = [ind for ind in indicators if lit.RED in ind]
        return colored_button_label, button_label, indicators

class lit:
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    BLACK = '\033[90m'
    ENDC = '\033[0m'

    @classmethod
    def random_color(cls):
        colors = [cls.RED, cls.BLUE, cls.YELLOW, cls.WHITE, cls.BLACK]
        return random.choice(colors)
