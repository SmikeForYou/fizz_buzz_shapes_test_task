MAX_VALUE = 100


class Strategy:
    def __init__(self, divider: int, number: int):
        self.divider = divider
        self.number = number

    def divide(self):
        return self.number % self.divider


class Printer:
    def __init__(self, print_word: str, strategy: Strategy):
        self.print_word = print_word
        self.strategy = strategy

    def condition_print(self):
        return self.strategy.divide() == 0


if __name__ == '__main__':
    for num in range(1, MAX_VALUE + 1):
        fizz_buzz_strategy = Strategy(15, num)
        fizz_strategy = Strategy(3, num)
        buzz_strategy = Strategy(5, num)
        default_strategy = Strategy(1, num)
        for printer in [Printer("FizzBuzz", fizz_buzz_strategy), Printer("Fizz", fizz_strategy),
                        Printer("Buzz", buzz_strategy), Printer(str(num), default_strategy)]:
            if printer.condition_print():
                print(printer.print_word)
                break
        else:
            raise RuntimeError(f"Unhandled case {num}")
