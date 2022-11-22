import sys, os
import shutil
import time
import glob
from colorama import init, Fore, Back, Style

LINE_ = Fore.RESET + "\n__________________________________________"

def OpenFile(file_name, mode):
        try:
            file = open(file_name, mode)
            return file
        except FileExistsError:
            print(Fore.RED + "Error! File exists." + Fore.RESET)
        except FileNotFoundError:
            print(Fore.RED + "Error! File does not exist" + Fore.RESET)

def WriteFile(file):
    user_input = " "
    print(Fore.GREEN + "Editor Active: " + Fore.RESET)
    while len(user_input) != 0:                             #while user_input is not blank, keep writing
        user_input = input()
        if user_input == "":
            break
        file.write(user_input + '\n')

def PrintFile(file):
    if file is not None:
        print()
        data = file.read().splitlines()
        print(LINE_)
        for line in data:
            print(line)
        print(LINE_)

def CloseFile(file):                            
    if file is not None:                        #if file is not opened, prevent closing
        file.close()

def PrintFilesInCurrentDirectory():
    data = os.listdir()
    i=0
    print("Files in the directory: " + Fore.YELLOW)
    for file in data:
        if file == "Text Operations.py":
            continue
        if i%3 == 0:
            print()
        print(file + "\t",end="")
        i+=1
    print(LINE_)



if __name__ == '__main__':

    choice = ""
    while True:

        os.system('cls')

        PrintFilesInCurrentDirectory()

        print(Fore.CYAN + "\nChoose an option:\n")
        print("1. Create new blank file")
        print("2. Read file")
        print("3. Write file (Re-write existing one / make new one)")
        print("4. Append text (to existing file / make new one)")
        print("5. Delete file")
        print("6. Exit program\n")

        choice = input("Choice: " + Fore.RESET)
        while choice not in ("1","2","3","4","5","6"):
            choice = input(Fore.CYAN + "Choice: " + Fore.RESET)

        if choice != '6':
            file_name = input(Fore.YELLOW + "\nEnter file name (example: file.txt): " + Fore.RESET)
            while file_name == "Text Operations.py":
                input(Fore.RED + "Access denied! Choose a file which is not this script: " + Fore.RESET)

        match choice:
            case "1":
                file = OpenFile(file_name, 'x')
                CloseFile(file)
            case "2":
                file = OpenFile(file_name, 'r')
                PrintFile(file)
                CloseFile(file)
            case "3":
                file = OpenFile(file_name, 'w')
                WriteFile(file)
                CloseFile(file)
            case "4":
                file = OpenFile(file_name, 'a')
                WriteFile(file)
                CloseFile(file)
            case "5":
                if os.path.exists(file_name) and file_name != 'Text Operations.py':
                    os.remove(file_name)
                    print(Fore.GREEN + "File deleted succesfully!" + Fore.RESET)
                else:
                    print(Fore.RED + "Error! File not found." + Fore.RESET)
            case "6":
                break

        input(Fore.CYAN + "\n\nInput any key to proceed" + Fore.RESET)


