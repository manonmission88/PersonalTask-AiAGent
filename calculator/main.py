import sys
from pkg.calculator import Calculator
from pkg.render import render


def main():
    calculator = Calculator()
    expression = "3 + 7 * 2"
    #result = calculator.evaluate(expression)
    #print(f"Result of '{expression}' is: {result}")
    #return

    #if len(sys.argv) <= 1:
    #    print("Calculator App")
    #    print('Usage: python main.py "<expression>"')
    #    print('Example: python main.py "3 + 5"')
    #    return

    #expression = " ".join(sys.argv[1:])
    try:
        result = calculator.evaluate(expression)
        to_print = render(expression, result)
        print(to_print)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()