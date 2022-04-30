from argparse import ArgumentParser
from calories_tracker.reusing.github import download_from_github
from os import remove

def replace_in_file(filename, s, r):
    data=open(filename,"r").read()
    remove(filename)
    data=data.replace(s,r)
    f=open(filename, "w")
    f.write(data)
    f.close()

parser=ArgumentParser()
parser.add_argument('--local', help='Parses files without download', action="store_true", default=False)
args=parser.parse_args()      

if args.local==False:
    download_from_github("turulomio", "reusingcode", "python/call_by_name.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "python/connection_pg.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "python/listdict_functions.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "django/decorators.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "python/lineal_regression.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "python/casts.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "python/currency.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "python/github.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "python/datetime_functions.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "python/text_inputs.py", "calories_tracker/reusing")
    download_from_github("turulomio", "reusingcode", "python/libmanagers.py", "calories_tracker/reusing")
    download_from_github("turulomio", "django_moneymoney", "moneymoney/request_casting.py", "calories_tracker/reusing")

replace_in_file("calories_tracker/reusing/casts.py", "from currency", "from .currency")
replace_in_file("calories_tracker/reusing/casts.py", "from percentage", "from .percentage")

replace_in_file("calories_tracker/reusing/listdict_functions.py", "from casts", "from .casts")

replace_in_file("calories_tracker/reusing/request_casting.py", ".reusing", "")