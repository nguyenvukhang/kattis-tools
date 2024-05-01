from __types__ import *

kat = Kattis()
kat.load("export.json")

# list of kattis usernames of students in class.
my_class_usernames = lines("secrets.txt") or []
kat.assert_valid_usernames(my_class_usernames)

print(kat.get_summary("t9spelling", my_class_usernames))
