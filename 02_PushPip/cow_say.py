import sys
from cowsay import cowsay, list_cows
import argparse

parser = argparse.ArgumentParser(prog="cowsay", description="Cowsay program")

parser.add_argument('message', nargs='?', default='', help='cow message')
args = parser.parse_args()

print(cowsay(message=args.message))
