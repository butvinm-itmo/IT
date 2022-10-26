from dataclasses import dataclass


class Token:
    ident: int


@dataclass
class OpenTag(Token):
    tag: str
    ident: int = 0


@dataclass
class CloseTag(Token):
    tag: str
    ident: int = 0


@dataclass
class TagValue(Token):
    tag: str
    value: str
    ident: int = 0
