import importlib
import pkgutil

def find_commands(base_package : str ='app.commands') -> dict:
    commands = {}
    for _ , command_name , _ in pkgutil.iter_modules([base_package.replace('.','/')]):
         commands[command_name] = base_package + '.' + command_name
    return commands
        

def run_command(command_name : str , *args, **kwargs):
     commands = find_commands()
     if command_name not in commands:
        print(f"  Unknown command: {command_name}")
        print('  Commands are :')
        for name , value in commands.items() :
            print(f'  {name}')
        return
     command_module = importlib.import_module((commands[command_name]))
     command_class = getattr(command_module, command_name.capitalize() + 'Command' , None)

     if not command_class:
        print(f"Invalid command: {command_name}")
        return
     
     command_instance = command_class()
     command_instance.run(*args , **kwargs)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2 :
        print('Please Provide a command')              
    else :
        command_name = sys.argv[1]
        args = sys.argv[2:]
        run_command(command_name , *args)


