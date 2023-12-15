import argparse

from mariadb import model


# Parser

parser = argparse.ArgumentParser()

parser.add_argument('--maria', type=str, help='initialise la base de données Maria DB.')

args = parser.parse_args()

if __name__ == "__main__":
    if args.maria : 
        