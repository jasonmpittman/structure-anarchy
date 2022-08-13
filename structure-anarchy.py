#!/usr/bin/env python3

# 
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

def loop():
    operation = inquirer.select(
        message="Select a bibliometric operation:",
        choices=[
            "Process PDF to Text",
            "Process Text to CSV",
            "Display CSV",
            Choice(value=None, name="Exit")
        ],
        default=None,
    ).execute()

    if operation == "Process PDF to Text":
        print("convert pdfs")

    if operation == "Process Text to CSV":
        print("convert to csv")

    if operation == "Display CSV":
        print("display it")

def main():
    loop()

    proceed = inquirer.confirm(message="Continue?", default=True).execute()
    if proceed:
        main()

if __name__ == "__main__":
    main()

