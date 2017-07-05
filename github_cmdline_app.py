#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    github_cmdline_app.py input <name>
    github_cmdline_app.py (-i | --interactive)
    github_cmdline_app.py (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""

import sys
import cmd
import requests
from docopt import docopt, DocoptExit


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class GithubInteractiveProgram(cmd.Cmd):
    intro = 'Welcome to my interactive program!' \
            + ': Type help for a list of commands.'
    prompt = '(Input github username) '
    file = None

    @docopt_cmd
    def do_input(self, arg):
        """Usage: input <name>"""
        name = arg['<name>']
        if name is not None:
            # The variable result stores github repos api for a particular user
            # obtained using the requests http client library
            result = requests.get('https://api.github.com/users/' + name + '/repos')

            # if request is successful, the function returns the list of repositories
            # in a user's github account
            if result.status_code == 200:
                repos = result.json()
                print('\t')
                print('REPOSITORIES:')
                for repo in repos:
                    print(repo['name'])

            # if request not successful, http code error code is returned
            else:
                print('HTTP ERROR %d.' % result.status_code)

        print('\t')
        print(arg)

    @staticmethod
    def do_quit(arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    GithubInteractiveProgram().cmdloop()

print(opt)
