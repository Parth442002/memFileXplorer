from PyInquirer import prompt
from termcolor import colored
from fileSystem import FileSystem
from questions import questions, exitQuestions
import pyfiglet
import re


def main():
    ascii_banner = pyfiglet.figlet_format(
        "In-Memory File System", font="small", width=100
    )
    print(ascii_banner)

    # FileSysten Instance
    system = FileSystem()

    answers = prompt(questions)

    if answers["load_session"]:
        system.load_session(answers["session_path"])
        print(colored("Loading the existing session.", "green"))
    else:
        print(colored("Creating a new Session"))

    # In-Memory File System
    print("\n")
    while True:
        user_input = input(f"${system.current_dir}> ")

        if user_input.lower() == "exit":
            exitAnswers = prompt(exitQuestions)
            if exitAnswers["save_session"]:
                system.save_session(exitAnswers["session_path"])
            print("Exiting...")
            break

        try:
            string = user_input.split()
            command = string[0]

            if command == "mkdir":
                system.mkdir(string[1])

            elif command == "ls":
                result = system.ls(string[1] if len(string) > 1 else "")
                print("\n".join(result))

            elif command == "cd":
                system.cd(string[1])

            elif command == "touch":
                system.touch(string[1])

            elif command == "echo":
                # Directly getting the string
                system.echo(user_input)

            elif command == "cat":
                system.cat(string[1])

            elif command == "rm":
                system.rm(string[1])

            elif command == "grep":
                if len(string) == 3:
                    match = re.match(r'^["\'](.+)["\']$', string[1])
                    pattern = match.group(1) if match else string[1]
                    system.grep(pattern, string[2])
                else:
                    print("Either the Pattern or filename is missing")

            elif command == "cp":
                if len(string) == 3:
                    system.cp(string[1], string[2])
                else:
                    print("Source/Desitnation Missing !")

            elif command == "mv":
                if len(string) == 3:
                    system.mv(string[1], string[2])
                else:
                    print("Source/Desitnation Missing !")
            else:
                print("Command not implemented !!!")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
