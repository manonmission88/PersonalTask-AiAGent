from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


def test():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)
    
    result = get_file_content("calculator", "main.py")
    print("Result for 'main.py' file:")
    print(result)
    
    result = get_file_content("calculator", "lorem.txt")
    print("Result for 'lorem.txt' file:")
    print(result)
    
    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for 'calculator.py' file:")
    print(result)


if __name__ == "__main__":
    test()