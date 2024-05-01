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


class Export(TypedDict):
    students: list[Student]
    assignments: list[Assignment]
    teachers: list[Teacher]


def subs(asm: Assignment) -> Iterator[tuple[str, Submission]]:
    """
    Create an iterator over the submissions of the assignment.
    Returns a tuple of (<Assignment Name>, <Submission>) each iterate.
    """
    for group in asm["groups"]:
        for asm_name, result in group["results"].items():
            for sub in result["submissions"]:
                yield asm_name, sub
