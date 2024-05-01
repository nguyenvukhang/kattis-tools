from __types__ import *

KATTIS_EXPORT_JSON_PATH = "export.json"

kat = Kattis()
kat.load(KATTIS_EXPORT_JSON_PATH)

# dict[<username>, dict[<assignment>, <verdict>]]
results: dict[str, dict[str, Verdict]] = {s["username"]: {} for s in kat.students}

# list of kattis usernames of students in class.
my_class_usernames = [
]

# for asm in assignments:
#     for asm_name, sub in subs(asm):
#         username = sub["submitting_user"]
#         user_data = results[username]
#         curr_verdict = user_data.get(asm_name, None)
#         if curr_verdict is None:
#             user_data[asm_name] = sub["verdict"]
#             continue
#         if v_rank(sub["verdict"]) >= v_rank(curr_verdict):
#             user_data[asm_name] = sub["verdict"]


def summarize(assignment: str, students: list[str]) -> dict[Verdict, list[str]]:
    summary: dict[Verdict, list[str]] = {v: [] for v in VERDICTS}

    for username in my_class_usernames:
        user_data = results[username]
        verdict = user_data.get("t9spelling", None)
        if verdict is not None:
            summary[verdict].append(username)
    return summary


print(kat.list_student_usernames())
