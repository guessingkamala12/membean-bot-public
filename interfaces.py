from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    pass

@dataclass
class MCQuestion(Question):
    question: str
    choices: List[str]
    def __str__(self):
        return f"{self.question}\nChoices: {self.choices}"

@dataclass
class FillInBlank(Question):
    maxLength: int
    firstLetter: str
    hint: str
    def __str__(self):
        return f"FillInBlank: Hint={self.hint}, First={self.firstLetter}, MaxLen={self.maxLength}"

@dataclass
class Constellation(Question):
    question: str
    options: List[str]
    def __str__(self):
        return f"Constellation: Question={self.question}, Options={self.options}"
