from fileSystem import FileSystem

# File System instance
system = FileSystem()

while True:
    user_input = input(f"{system.current_dir}> ")

    if user_input.lower() == "exit":
        # fs.save_state()
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

        else:
            print("Command not implemented !!!")

    except Exception as e:
        print(f"Error: {str(e)}")
