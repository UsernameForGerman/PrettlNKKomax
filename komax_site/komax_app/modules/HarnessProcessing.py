# Everithing with harness number check

def is_digit(symbol: str):
    if symbol >= '0' and symbol <= '9':
        return True
    else:
        return False


def is_letter(symbol: str):
    symbol_lower = symbol.lower()
    if (symbol_lower >= 'a' and symbol_lower <= 'z') or (symbol_lower >= 'а' and symbol_lower <= 'я'):
        return True
    else:
        return False

class HarnessNumber():
    harness_number = None

    def __init__(self, harness_number):
        self.harness_number = harness_number

    def check_harness_number(self):
        if type(self.harness_number) is int:
            return True
        elif type(self.harness_number) is str:
            for symbol in self.harness_number:
                if is_digit(symbol) or is_letter(symbol) or symbol == '-' or symbol == '.':
                    continue
                else:
                    return False

            return True
        else:
            return False
