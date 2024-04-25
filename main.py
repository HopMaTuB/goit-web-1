from classes import AddressBook, Record, SimpleView,TableView,UserView
import pickle
import const


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Enter the argument for the command"
        except Exception as e:
            return f"{e}"
    return inner
     
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def save_data(book,filename="addressbook.pkl"): 
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 
    
@input_error
def add_birthday(args, book:AddressBook):
    name, date = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(date)
    return 'Birthday added'

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Name Not Found"
    return record.birthday

@input_error
def birthdays(args,book: AddressBook):
    return book.get_upcoming_birthdays()    

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)              
        book.add_record(record)        
    record.add_phone(phone)
    return "Contact added"

@input_error
def change_contact(args, book:AddressBook):
    name,old_phone,new_phone = args
    record = book.find(name)
    if not record:
        return "Name Not Found"    
    record.edit_phone(old_phone,new_phone)
    return "Contact updated"

@input_error   
def phone_username(args, book:AddressBook):
    phone = args[0]
    record = book.find(phone)
    if not record:
        return "Contact Not Found"
    return '; '.join(str(phone) for phone in record.phones)

@input_error
def show_all(args,book:AddressBook):
    return book   

@input_error
def all_commands():
    return const.commands

def choose_view():
    """Prompt the user to choose a view."""
    while True:
        choice = input("Choose view (simple/table): ").strip().lower()
        if choice == 'simple':
            return SimpleView()
        elif choice == 'table':
            return TableView()
        else:
            print("Invalid choice. Please choose 'simple' or 'table'.")


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    view = choose_view()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "all":
            view.display_message(show_all(args,book))
        elif command == "hello":
            print("How can I help you?")
        elif command == "change":
            view.display_message(change_contact(args, book))
        elif command == "add":
            view.display_message(add_contact(args, book))
        elif command == "phone":
            view.display_message(phone_username(args,book))
        elif command == "birthday":
            view.display_message(show_birthday(args, book))
        elif command == "birthdays":
            view.display_message(birthdays(args, book))
        elif command == "add-birthday":
            view.display_message(add_birthday(args, book))
        elif command == "all_commands":
            view.display_message(all_commands(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()