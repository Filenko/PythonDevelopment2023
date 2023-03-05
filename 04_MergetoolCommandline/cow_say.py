import cowsay
import shlex
import cmd

def ParseArgs(args):
    return shlex.split(args)

class DiyCowsay(cmd.Cmd):
    prompt = ">>> "

    def do_cowsay(self, args):
        message = ParseArgs(args)[0]
        print(cowsay.cowsay(message, cow = "default", eyes = "oO", tongue = " "))


    def do_exit(self, args):
        return True

    def emptyline(self):
        pass


if __name__ == "__main__":
    DiyCowsay().cmdloop()