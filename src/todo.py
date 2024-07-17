import argparse
from todofile import TodoFile, logging, Path, datetime

VERSION = "0.0.1"
DEFAULT_DIR = ".tododb"
DEFAULT_FILENAME = "data.json"

DEFAULT_LOGFILE = "debug.log"
logging.basicConfig(filename=Path(DEFAULT_DIR).joinpath(DEFAULT_LOGFILE))

# expl: not sure what these do below, using defaults for now
# PROG = "python todo.py"
# DESCRIPTION = "Manage a todolist in your current directory in the spirit of Git :-)"
# PARSER = argparse.ArgumentParser(prog=PROG, description=DESCRIPTION)
# 

PARSER = argparse.ArgumentParser()

def version():
    print(f"version = {VERSION}")


def init(dirname=DEFAULT_DIR, filename=DEFAULT_FILENAME) -> bool:
    res = False
    try:
        todofile = TodoFile(dirname, filename)
        logging.debug(f"created todofile from init: {todofile}")
        res = True

    except Exception as ex:
        logging.error("TodoFile creation failed in init()")
        raise RuntimeError("app encountered an error") from ex
    return res


def ls(dirname=DEFAULT_DIR, filename=DEFAULT_FILENAME) -> bool:
    todofile = TodoFile(dirname, filename)
    d = todofile.getdata()
    print("TODO-LIST " + "-" * 69)
    print("Active tasks:")
    [print(f"[ ] - {t['text']}") for t in d["active_tasks"]]
    print("Complete tasks:")
    [print(f"[Y] - {t['text']}") for t in d["complete_tasks"]]
    print("-" * 69 + " TODO-LIST")
    return True


def dump(dirname=DEFAULT_DIR, filename=DEFAULT_FILENAME) -> None:
    # dev use only
    todofile = TodoFile(dirname, filename)
    print(todofile)


def add(todostr, dirname=DEFAULT_DIR, filename=DEFAULT_FILENAME) -> None:
    todofile = TodoFile(dirname, filename)
    todofile.push(todostr)


def complete(q, dirname=DEFAULT_DIR, filename=DEFAULT_FILENAME) -> None:
    todofile = TodoFile(dirname, filename)
    todofile.strike(q)


def main_hid():
    init()  # TODO re-init should inform its already present, maybe also list;
    ls()
    # dump()
    version()


def main() -> bool:

    # TODO: move me to tests
    # init()
    # ls()
    # add(f"test addition task: {datetime.now()}")
    # ls()
    # complete("addition")
    # ls()
    # dump()
    # exit(0)
    # TODO fix this lame arg parsing, re read docs and proceed...

    PARSER.add_argument(
        "action",
        choices=["init", "list", "add", "remove", "dump"],
        help="commands available: init, list, add, remove",
    )

    #TODO: this should only be considered with remove...
    PARSER.add_argument("-s", "--search-value", help="search string to match against existing tasks")
    args = PARSER.parse_args()

    if args.action == None:
        PARSER.print_usage()
        return True

    if args.action == "init":
        print("init execd")
    elif args.action == "list":
        ls() 
        print("list execd")
    elif args.action == "add":
        print("add execd")
    elif args.action == "remove":
        print("remove execd")
    else:
       PARSER.print_usage() 

    logging.debug("exiting main")
    return True


if __name__ == "__main__":
    main()
