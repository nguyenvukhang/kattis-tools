import json
from __types__ import *

KATTIS_EXPORT_JSON_PATH = "export.json"

data: Export = {}

with open(KATTIS_EXPORT_JSON_PATH, "r") as f:
    data = json.load(f)
    for s in data["students"]:
        s["email"] = s["email"].lower()

assignments = data["assignments"]
students = data["students"]


# dict[<username>, dict[<assignment>, <verdict>]]
results: dict[str, dict[str, Verdict]] = {s["username"]: {} for s in data["students"]}


for asm in assignments:
    for asm_name, sub in subs(asm):
        username = sub["submitting_user"]
        user_data = results[username]
        curr_verdict = user_data.get(asm_name, None)
        if curr_verdict is None:
            user_data[asm_name] = sub["verdict"]
            continue
        if v_rank(sub["verdict"]) >= v_rank(curr_verdict):
            user_data[asm_name] = sub["verdict"]

print(results)
