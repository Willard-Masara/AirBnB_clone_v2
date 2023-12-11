import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pline = line[:]
            _cls = pline[:pline.find('.')]
            _cmd = pline[pline.find('.') + 1:pline.find('(')]

            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].replace('\"', '')
                pline = pline[2].strip()
                if pline:
                    if pline[0] is '{' and pline[-1] is'}' and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        exit()

    def help_quit(self):
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        print()
        exit()

    def help_EOF(self):
        print("Exits the program without formatting\n")

    def emptyline(self):
        pass

    def do_create(self, args):
        """ Create an object of any class with given parameters"""
        if not args:
            print("** class name missing **")
            return

        class_name, *params = args.split()

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        param_dict = {}

        for param in params:
            try:
                key, value = param.split('=')

                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('\\"', '"').replace('_', ' ')
                elif '.' in value:
                    value = float(value)
                else:
                    value = int(value)

                param_dict[key] = value

            except ValueError:
                print(f"Skipping invalid parameter: {param}")

        new_instance = HBNBCommand.classes[class_name](**param_dict)
        storage.save()
        print(new_instance.id)
        storage.save()

    def help_create(self):
        print("Creates a class of any type")
        print("[Usage]: create <className> <param1>=<value1> <param2>=<value2> ...\n")

    def do_show(self, args):
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")



if __name__ == "__main__":
    HBNBCommand().cmdloop()

