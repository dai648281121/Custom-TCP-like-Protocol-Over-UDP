import sender
import receiver
import threading


def print_help():
    help_text = """
Commands may be abbreviated. Commands are:
connect connect to remote myftp
put     send file
get     receive file
quit    exit myftp
?       print help information
"""
    print(help_text)


def start_receiver():
    recv_thread = threading.Thread(target=receiver.main)
    recv_thread.start()


def put_file(filepath):
    try:
        sender.main(filepath)
    except Exception as e:
        print(f"Error sending file: {e}")


def get_file():
    print("Receiver is already running. Any incoming files will be saved.")


def main():
    start_receiver()
    print("Welcome to myftp!")
    print_help()
    while True:
        input_cmd = input("myftp> ").strip()
        cmd_parts = input_cmd.split(maxsplit=1)
        command = cmd_parts[0].lower()

        if command == 'quit':
            print("Exiting myftp")
            break
        elif command == 'put':
            if len(cmd_parts) == 2:
                filepath = cmd_parts[1]
                put_file(filepath)
                print()
            else:
                print("Usage: put <filename>")
        elif command == 'get':
            get_file()
        elif command == '?':
            print_help()
        else:
            print("Unknown command. Type '?' for help.")


if __name__ == "__main__":
    main()
