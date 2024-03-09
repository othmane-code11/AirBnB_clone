#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import shlex
import re
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State


def split_the_curly_braces(ext_arg):
    """Splits the curly braces for the update method."""
    th_curly_braces = re.search(r"\{(.*?)\}", ext_arg)

    if th_curly_braces is not None:
        id_with_a_comma = shlex.split(ext_arg[:th_curly_braces.span()[0]])
        id = [x.strip(",") for x in id_with_a_comma][0]
        t_str_data = th_curly_braces.group(1)

        try:
            ag_dict = ast.literal_eval("{" + t_str_data + "}")
        except Exception:
            print('**  invalid dictionary format **')
            return

        return id, ag_dict
    else:
        comnds = ext_arg.split(",")
        if comnds:
            try:
                id = comnds[0]
            except Exception:
                return "", ""
            try:
                attrbt_name = comnds[1]
            except Exception:
                return id, ""
            try:
                attrbt_value = comnds[2]
            except Exception:
                return id, attrbt_name
            return f"{id}", f"{attrbt_name} {attrbt_value}"


class HBNBCommand(cmd.Cmd):
    """Defines the HBNBCommand class.

    Attributes:
        prompt (str): The command prompt.
    """
    prompt = "(hbnb) "
    a_v_classes = \
        ["BaseModel", "User", "Amenity", "Place", "Review", "State", "City"]

    def emptyline(self):
        """Do nothing upon receiving an empty plus enter."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def help_quit(self, arg):
        """the help_quit to print decreption"""
        print('Quit command to exit the program')

    def do_EOF(self, arg):
        """Exist the console using Ctrl + D."""
        print("")
        return True

    def do_create(self, arg):
        """creates a new object and saves it"""
        comnds = shlex.split(arg)

        if len(comnds) == 0:
            print("** class name missing **")
        elif comnds[0] not in self.a_v_classes:
            print("** class doesn't exist **")
        else:
            nw_inst = eval(f'{comnds[0]}()')
            storage.save()
            print(nw_inst.id)

    def do_show(self, ag):
        """
        Prints the string representation of an instance
        based on name & id.
        """
        comnds = shlex.split(ag)

        if len(comnds) == 0:
            print("** class name missing **")
        elif comnds[0] not in self.a_v_classes:
            print("** class doesn't exist **")
        elif len(comnds) < 2:
            print("** instance id missing **")
        else:
            t_objcts = storage.all()

            ky = f"{comnds[0]}.{comnds[1]}"
            if ky in t_objcts:
                print(t_objcts[ky])
            else:
                print('** no instance found **')

    def do_destroy(self, ag):
        """
        Delete a class instance of a given id.
        Usage: destroy <class_name> <id>
        """
        comnds = shlex.split(ag)

        if len(comnds) == 0:
            print("** class name missing **")
        elif comnds[0] not in self.a_v_classes:
            print("** class doesn't exist **")
        elif len(comnds) < 2:
            print("** instance id missing **")
        else:
            t_objcts = storage.all()
            ky = f"{comnds[0]}.{comnds[1]}"
            if ky in t_objcts:
                del t_objcts[ky]
                storage.save()
            else:
                print('** no instance found **')

    def do_all(self, arg):
        """
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        t_objcts = storage.all()
        comnds = shlex.split(arg)

        if len(comnds) == 0:
            for ky, val in t_objcts.items():
                print(str(val))
        elif comnds[0] not in self.a_v_classes:
            print("** class doesn't exist **")
        else:
            for ky, val in t_objcts.items():
                if ky.split('.')[0] == comnds[0]:
                    print(str(val))

    def do_update(self, ag):
        """
        updates an instance based on the class name and id by adding or
        updating attribute and saves the change into the JSON file
        """
        comnds = shlex.split(ag)

        if len(comnds) == 0:
            print("** class name missing **")
        elif comnds[0] not in self.a_v_classes:
            print("** class doesn't exist **")
        elif len(comnds) < 2:
            print("** instance id missing **")
        else:
            t_objcts = storage.all()

            ky = f"{comnds[0]}.{comnds[1]}"
            if ky not in t_objcts:
                print("** no instance found **")
            elif len(comnds) < 3:
                print("** attribute name missing **")
            elif len(comnds) < 4:
                print("** value missing **")
            else:
                objt = t_objcts[ky]
                the_crly_braces = re.search(r"\{(.*?)\}", ag)

                if the_crly_braces:
                    try:
                        t_str_data = the_crly_braces.group(1)
                        ag_dict = ast.literal_eval("{" + t_str_data + "}")
                        attbt_names = list(ag_dict.keys())
                        attbt_values = list(ag_dict.values())
                        try:
                            setattr(objt, attbt_names[0], attbt_values[0])
                        except Exception:
                            pass

                        try:
                            setattr(objt, attbt_names[1], attbt_values[1])
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:
                    at_name = comnds[2]
                    at_value = comnds[3]
                    try:
                        at_value = eval(at_value)
                    except Exception:
                        pass
                    setattr(objt, at_name, at_value)
                objt.save()

    def do_count(self, ag):
        """prints the count of all instances based the class name."""
        t_objcts = storage.all()
        comnds = shlex.split(ag)

        if ag:
            the_cls_name = comnds[0]
        i = 0

        if comnds:
            if the_cls_name in self.a_v_classes:
                for objt in t_objcts.values():
                    if objt.__class__.__name__ == the_cls_name:
                        i += 1
                print(i)
            else:
                print('** invalid class name **')
        else:
            print("** class name missing **")

    def default(self, arg):
        """
        Default behavior  for the cmd module when input is  invalid.
        """
        argg_lst = arg.split('.')
        the_cls_name = argg_lst[0]
        comnd = argg_lst[1].split('(')
        the_cmd_methd = comnd[0]
        ext_arg = comnd[1].split(')')[0]

        mthd_dict = {
                'all': self.do_all,
                'destroy': self.do_destroy,
                'show': self.do_show,
                'count': self.do_count,
                'update': self.do_update
                }

        if the_cmd_methd in mthd_dict.keys():
            if the_cmd_methd != "update":
                return mthd_dict[the_cmd_methd](f"{the_cls_name} {ext_arg}")
            else:
                if not the_cls_name:
                    print("** class name missing **")
                    return
                try:
                    objt_id, ag_dict = split_the_curly_braces(ext_arg)
                except Exception:
                    pass
                try:
                    calling = mthd_dict[the_cmd_methd]
                    return calling(f"{the_cls_name} {objt_id} {ag_dict}")
                except Exception:
                    pass
        else:
            print(f"*** Unknown syntax: {arg}")
            return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
