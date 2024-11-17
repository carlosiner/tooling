import argparse
from os import path, makedirs
from shutil import copy
import re
from colorama import Fore, Style, init


# Define global path variables
path_workspace = ""

def set_up_directory(ticket):
    path_combo = path_workspace + ticket + "/"
    if not path.exists(path_combo):
        makedirs(ticket)
        copy(path_workspace+R"README.md", path_combo)
        print("✅ Folder generated!")
    else:
        print("✋ Folder already exists")

def checker_ticket(ticket):
    path_combo = path_workspace + ticket + "/"
    if path.exists(path_combo):
        with open(path_combo+"README.md", 'r') as file:
            content = file.read()
            case_section = re.search(r'(# General information.*?)(?=\n# |\Z)', content, re.DOTALL)
            if case_section:
                case_content = case_section.group(1)
                match_name = re.search(r'\*\*Name\*\*\:\s*(.*)', case_content)
                match_case = re.search(r'\*\*Case\*\*\:\s*(.*)', case_content)
                match_desc = re.search(r'\*\*Short Description\*\*\:\s*(.*)', case_content)
                if match_name and match_case and match_desc :
                    print(f"{Fore.GREEN}➤ Name: {Style.RESET_ALL}{match_name.group(1)}")
                    print(f"{Fore.GREEN}➤ Case: {Style.RESET_ALL}{match_case.group(1)}")
                    print(f"{Fore.GREEN}➤ Short Description: {Style.RESET_ALL}{match_desc.group(1)}")
                else:
                    raise ValueError("Name/Case/Description section not found in README.md")
            else:
                raise ValueError("# CASE section not found in README.md")
    else:
        raise ValueError(f"README.md not found in {ticket} directory")


def main():

    parser = argparse.ArgumentParser(
        exit_on_error=False,
        prog='Workspace Organizer',
        description='Enables a working path to work in the current item',
        epilog='--------'
    )

    ## Arguments definition
    parser.add_argument('-n', '--new', help="Defines a new ticket workspace")
    parser.add_argument('-c', '--check', help="Provides status over a ticket if exists")

    args = parser.parse_args()

    try: 
        ## Arguments selection 
        if args.new:
            set_up_directory(args.new)
        elif args.check:
            checker_ticket(args.check)
        else:
            raise ValueError("Please, provide an argument and a ticket to inspect")
    except Exception as e: 
        print(f"❌ Error: {e}")
        exit(1)


## * Main point 
if __name__ == "__main__":
    main()