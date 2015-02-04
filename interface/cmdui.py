#This file is part of REXT
#cmdui.py - command line interface script
#Author: Ján Trenčanský
#License: ADD LATER

import cmd
import core.utils
import core.globals
import core.Harvester

from core import loader


class Interpreter(cmd.Cmd):
    #
    modules = {}
    active_module = modules
    active_module_import_name = ""

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ">"
        #Load banner
        with open("./interface/banner.txt", "r") as file:
            banner = ""
            for line in file.read():
                banner += line
            self.intro = banner
            file.close()
        #Load list of available modules in modules
        module_directory_names = core.utils.list_dirs("./modules")  # List directories in module directory
        for module_name in module_directory_names:
            path = "./modules/" + module_name
            vendors = core.utils.list_dirs(path)
            vendors_dict = {}
            for vendor in vendors:
                vendor_path = path + "/" + vendor
                files = core.utils.list_files(vendor_path)
                vendors_dict[vendor] = files
            self.modules[module_name] = vendors_dict

    def emptyline(self):
        pass

    def postloop(self):
        print("Bye!")

    def do_exit(self, args):
        return True

    #Interpreter commands section

    def do_show(self, module):
        if module == "":
            if isinstance(self.active_module, dict):
                for key in self.active_module.keys():
                    print(key)
            elif isinstance(self.active_module, set):
                for file in self.active_module:
                    print(file)
        elif module == "modules":
            for key in self.modules.keys():
                print(key)
        elif module in self.modules.keys():
            for key in self.modules.get(module).keys():
                print(key)
        elif (self.active_module is dict) and (module in self.active_module.keys()):
            for key in self.active_module.get(module):
                print(key)
        else:
            print("Invalid argument for command show", module)

    def do_load(self, module):
        if isinstance(self.active_module, set):
            core.globals.active_script = module
            module_path = core.globals.active_module_path + module
            self.active_module_import_name = core.utils.make_import_name(module_path)
            loader.load_module(self.active_module_import_name)  # Module is loaded and executed
            loader.delete_module(self.active_module_import_name)  # Module is unloaded so it can be used again
            core.globals.active_module_import_name = ""
        elif isinstance(self.active_module, dict):
            if module in self.active_module.keys():
                self.active_module = self.active_module.get(module)
                core.globals.active_module_path += module + "/"
                core.utils.change_prompt(self, core.globals.active_module_path)

    def do_unload(self, e):
        core.globals.active_module = self.modules
        core.utils.change_prompt(self, None)
        core.globals.active_module_path = ""

    #Help to commands section

    def help_show(self):
        print("List available modules and vendors:")

    def help_load(self):
        print("load command help")

    def help_exit(self):
        print("Exit REXT")

