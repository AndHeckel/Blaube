from functions.get_files_info import get_files_info

def print_result(directory):
    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")
    print(get_files_info("calculator", directory))

print_result(".")
print_result("pkg")
print_result("/bin")
print_result("../")