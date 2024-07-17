from pathlib import Path
import json
from datetime import datetime
import logging


class TodoFile:
    """TodoFile is a fileobject storing todo info as json, inside a hidden dir
    default values are dir .tododb, file is data.json
    """

    # TODO: new lines in json try to fix ambiguity... also in __str___
    def __init__(self, dirname=".tododb", filename="data.json"):
        logging.info(" inside __init__ in todofile.py")

        fp = Path(dirname) / filename
        if not Path(dirname).exists():
            Path(dirname).mkdir()
        elif fp.exists():  # TODO:  check wellformed db file...
            self.datafilehandle = fp
            logging.debug("returning early since db already was present")
            return None

        if not fp.exists():
            fp.touch()

        with open(fp, "w") as fhandle:
            current_timestamp = datetime.now().strftime("%a %d %b %Y, %I:%M%p")
            json.dump(
                {
                    "id": "magixtoken",
                    "created_at": current_timestamp,
                    "updated_at": current_timestamp,
                    "active_tasks": [],
                    "complete_tasks": [],
                },
                fhandle,
            )

        self.datafilehandle = fp

        logging.debug("returning from constructor todofile()")

    # TODO: describe
    def __str__(self) -> str:
        response = None
        with open(self.datafilehandle) as fhandle:
            js_str = fhandle.read()
            response = json.dumps(
                js_str,
                sort_keys=False,
                indent=4,
                ensure_ascii=True,
                separators=(",", ":"),
            )
        return response

    # TODO: describe
    def getdata(self) -> object:
        response = None
        with open(self.datafilehandle) as fhandle:
            response = json.loads(fhandle.read())

        return response

    # TODO: describe
    def push(self, todostr) -> bool:
        r = None
        with open(self.datafilehandle) as fhandle:
            r = json.loads(fhandle.read())

        current_time = datetime.now().ctime()
        todoobj = {"id": current_time, "text": todostr}
        r["active_tasks"].append(todoobj)
        creation_time = r["created_at"]
        with open(self.datafilehandle, "w") as fhandle:
            current_timestamp = datetime.now().strftime("%a %d %b %Y, %I:%M%p")
            json.dump(
                {
                    "id": "magixtoken",
                    "created_at": creation_time,
                    "updated_at": current_timestamp,
                    "active_tasks": r["active_tasks"],
                    "complete_tasks": r["complete_tasks"],
                },
                fhandle,
            )

        logging.debug("returning from push()")

        return True

    # TODO: describe
    def strike(self, qstr) -> bool:
        r = None
        with open(self.datafilehandle) as fhandle:
            r = json.loads(fhandle.read())

        dbcreation_time = r["created_at"]
        current_time = datetime.now().ctime()
        ts = r["active_tasks"]
        struck = [t for t in ts if qstr in t["text"]]
        if len(struck) == 0:
            print(f"{qstr} not found in active tasks")
            return True

        ts_new = ts
        for s in struck:
            if len(ts_new) <= 0:
                break
            r["complete_tasks"].append(s)
            ts_new.remove(s)

        r["active_tasks"] = ts_new

        with open(self.datafilehandle, "w") as fhandle:
            current_timestamp = datetime.now().strftime("%a %d %b %Y, %I:%M%p")
            json.dump(
                {
                    "id": "magixtoken",
                    "created_at": dbcreation_time,
                    "updated_at": current_time,
                    "active_tasks": r["active_tasks"],
                    "complete_tasks": r["complete_tasks"],
                },
                fhandle,
            )
        logging.debug("returning form strike() in db")

        return True
