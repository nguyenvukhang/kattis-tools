from collections.abc import Iterator
from typing import TypedDict, Literal, get_args

# Order of definition matters, since this will be used in `v_rank()`.
Verdict = Literal[
    "New",  # New submission
    "Running",  # Running
    "CE",  # Compile Error
    "RTE",  # Runtime Error
    "WA",  # Wrong Answer
    "MLE",  # Memory Limit Exceeded
    "TLE",  # Time Limit Exceeded
    "OLE",  # Output Limit Exceeded
    "AC",  # Accepted
]
VERDICTS = get_args(Verdict)


def v_rank(v: Verdict) -> int:
    """
    Gets the rank of the verdict. Higher ranks are more favorable.
    ACCEPTED gets the highest rank.
    """
    return VERDICTS.index(v)


class Student(TypedDict):
    username: str
    name: str
    non_anonymous: bool
    email: str


class Teacher(TypedDict):
    username: str
    name: str
    teaching_assistant: bool


class Submission(TypedDict):
    submission_id: int
    time: int
    real_time: float
    submitting_user: str
    verdict: Verdict


class GroupResult(TypedDict):
    submission_count: int
    submissions: list[Submission]


class Group(TypedDict):
    group_name: str
    solved_count: int
    members: list[str]
    results: dict[str, GroupResult]


class Problem(TypedDict):
    submission_count: int
    submissions: list[Submission]


class Assignment(TypedDict):
    groups: list[Group]
    length: str
    name: str
    problems: list[Problem]
    starttime: int


class Kattis:
    def __init__(self) -> None:
        self.students: list[Student] = []
        self.assignments: list[Assignment] = []
        self.teachers: list[Teacher] = []

    def load(self, kattis_json_path: str):
        from json import load

        with open(kattis_json_path, "r") as f:
            data = load(f)
            self.students = data["students"]
            self.assignments = data["assignments"]
            self.teachers = data["teachers"]

            for s in self.students:
                s["email"] = s["email"].lower()

    def list_student_usernames(self) -> list[str]:
        return [s["username"] for s in self.students]

    def list_assignments(self) -> list[str]:
        """
        Lists all the unique assignment names found in the database.
        """
        assignments = set()
        for asm in self.assignments:
            for group in asm["groups"]:
                for assignment in group["results"].keys():
                    assignments.add(assignment)
        return list(assignments)

    def subs(self) -> Iterator[tuple[str, Submission]]:
        """
        Create an iterator over the submissions of the assignment.
        Returns a tuple of (<Assignment Name>, <Submission>) each iterate.
        """
        for asm in self.assignments:
            for group in asm["groups"]:
                for asm_name, result in group["results"].items():
                    for sub in result["submissions"]:
                        yield asm_name, sub
