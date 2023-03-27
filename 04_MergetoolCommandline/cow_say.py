import cowsay
import cmd
import readline
import shlex


class CowShell(cmd.Cmd):
    intro = 'Welcome!'
    prompt = '<cow> '

    def do_make_bubble(self, args):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        make_bubble text [-b cowsay | cowthink] [-d width] [-w wrap_text]

        text: text
        brackets=cowsay
        width=40
        wrap_text=True
        """
        parsed = shlex.split(args)
        if len(parsed) == 0:
            print('Wrong arguments')
            return

        text, *optional_params = parsed

        params = {"brackets": cowsay.THOUGHT_OPTIONS["cowsay"], "width": 40, "wrap_text": True}
        for i in range(0, len(optional_params), 2):
            match optional_params[i]:
                case '-w':
                    params["width"] = int(optional_params[i + 1])
                case '-b':
                    params["brackets"] = cowsay.THOUGHT_OPTIONS[optional_params[i + 1]]
                case '-t':
                    params["wrap_text"] = bool(optional_params[i + 1])
                case _:
                    print('Wrong arguments')
                    return

        print(cowsay.make_bubble(text, **params))

    def complete_make_bubble(self, text, line, begidx, endidx):
        options = {'-b', '-w', '-t'}
        parsed = shlex.split(line)

        match parsed[-1]:
            case '-b':
                return ['cowsay', 'cowthink']
            case '-w':
                return ['20', '40', '60', '80']
            case '-t':
                return ['True', 'False']
            case _:
                if parsed[-2] == '-b' and text:
                    return [x for x in ['cowsay', 'cowthink'] if x.startswith(parsed[-1])]
                return list(options - set(parsed))

    def do_list_cows(self, args):
        """Lists all cows"""
        if args:
            print(cowsay.list_cows(args))
        else:
            print(cowsay.list_cows())

    def do_cowsay(self, args):
        """
        Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string
        cowsay message [-e eye_string] [-c cow] [-t tongue_string]

        :message: message
        :cow: -f - all cows
        :eyes: -e - eyes
        :tongue: -t - tongue
        """
        return self.cowThinkOrSay(args, cowsay.cowsay)

    def complete_cowsay(self, text, line, begidx, endidx):
        parsed = shlex.split(line)
        options = {'-f', '-e', '-t'}
        option = parsed[-1] if parsed[-1] in options or not text else parsed[-2]
        match option:
            case '-f':
                cows = cowsay.list_cows()
                return [cow for cow in cows if cow.startswith(text)]
            case '-e':
                eyes = ['oo', 'o_O', '$_$', '$$', '--', '**', '..']
                return [eye for eye in eyes if eye.startswith(text)]
            case '-t':
                tongues = ['U ', ' u', 'u ', '||']
                return [tongue for tongue in tongues if tongue.startswith(text)]
            case _:
                return []

    def do_cowthink(self, args):
        """
        Returns the resulting cowthink string.
        cowthink message [-e eye_string] [-c cow] [-T tongue_string]

        message: The message to be displayed
        cow: -f – all cows
        eyes: -e
        tongue: -t
        """
        return self.cowThinkOrSay(args, cowsay.cowthink)

    def cowThinkOrSay(self, args, func):
        parsed = shlex.split(args)
        if len(parsed) == 0:
            print('Wrong arguments')
            return

        message, *optional_params = parsed

        params = {'cow': 'default', 'eyes': cowsay.Option.eyes, 'tongue': cowsay.Option.tongue}
        for i in range(0, len(optional_params), 2):
            match optional_params[i]:
                case '-f':
                    params["cow"] = optional_params[i + 1]
                case '-e':
                    params["eyes"] = optional_params[i + 1]
                case '-t':
                    params["tongue"] = optional_params[i + 1]
                case _:
                    print('Wrong arguments')
                    return

        print(func(message, **params))

    def complete_cowthink(self, text, line, begidx, endidx):
        return self.complete_cowsay(text, line, begidx, endidx)


if __name__ == '__main__':
    CowShell().cmdloop()
