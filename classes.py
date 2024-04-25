from datetime import datetime, timedelta
import datetime
from collections import UserDict
import const
from abc import ABC, abstractmethod

class Field:
    def __init__(self, value):
        self.value = value
    
    def is_valid(self,value):
        return True
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self,value):
        if not self.is_valid(value):
            raise ValueError
        else:
            self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def if_valid(self,value):
        return bool(value)


class Phone(Field):
    def is_valid(self,value):
        return len(value)==10 and value.isdigit()

        
class Birthsday(Field):        
    def is_valid(self,value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except:
            return False
        return True
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self,value):
        if not self.is_valid(value):
            raise ValueError
        else:
            self.__value = datetime.strptime(value, "%d.%m.%Y").date()
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value):
        number=Phone(value) 
        if len(value) == 10 and value.isdigit():
            self.phones.append(number)

    def add_birthday(self,birthday):
        self.birthday = Birthsday(birthday)
        return self.birthday

    def remove_phone(self,phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
    
    def edit_phone(self, phone: str, new_phone: str):
        if self.find_phone(phone):
            self.remove_phone(phone)
            self.add_phone(new_phone)
        else:
            raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p                  

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {(self.birthday)}"

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)


    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        tdate=datetime.today().date()
        birthdays=[]

        for user in self.data.values():
            if user.birthday:
                birthday = user.birthday.value.replace(year=tdate.year)
                if birthday < tdate:
                    birthday = birthday.replace(year=tdate.year + 1)

                days_until_birthday = (birthday - tdate).days

                if 0 <= days_until_birthday < 7:
                    if birthday.weekday() >= 5:
                        birthday += timedelta(days=(7 - birthday.weekday()))

                    birthdays.append({
                        'name': user.name.value,
                        'congratulation': birthday.strftime('%d.%m.%Y')
                        })
        return birthdays      

        

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

class UserView(ABC):

    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_commands(self):
        pass

    @abstractmethod
    def display_message(self, message):
        pass

class SimpleView(UserView):

    def display_contacts(self, contacts):
        print("Contacts:")
        for contact in contacts:
            print(contact)

    def display_commands(self):
        print(const.commands)

    def display_message(self, message):
        print(message)

class TableView(UserView):

    def display_contacts(self, contacts) -> None:
        """Display contacts as a table."""
        print("Contacts:")
        if not contacts:
            print("No contacts found.")
            return

        table_width = const.name_lenght + const.phone_lenght + const.birthday_lenght + 10 # 10 - just fix for the table width

        print("-" * table_width)
        print(f"| {'Name':<{const.name_lenght}} | {'Phone Numbers':<{const.phone_lenght}} | {'Birthday':<{const.birthday_lenght}} |")
        print("-" * table_width)

        for contact in contacts.data.values():
            name = contact.name.value
            phones = ';'.join(str(p) for p in contact.phones)
            birthday = str(contact.birthday) if contact.birthday else "None"
            print(f"| {name:<{const.name_lenght}} | {phones:<{const.phone_lenght}} | {birthday:<{const.birthday_lenght}} |")

        print("-" * table_width)

    def display_commands(self) -> None:
        print(const.commands)

    def display_message(self, message) -> None:
        print(message)


