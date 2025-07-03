from typing import Tuple, Union
import re


VERSION_PATTERN = r'''
[a-fA-F0-9]{6,}       # hex-строка (6+ символов)
|[a-zA-Z]+            # слово
|\d+                 # число
'''


class Version:
    _key: Tuple[
        int, 
        Union[str, int],
        Union[str, int]
    ]

    def __init__(self, epoch: int, version: str, release: str):
        self.epoch = epoch
        self.version = version.lower()
        self.release = release.lower()

        self._validation()

    def _ishex(self, s: str) -> bool:
        pattern = r"^[0-9a-fA-F]+$"
        return bool(re.match(pattern, s))

    def _separate_and_classify(self, token: str) -> list[str]:
        parts = []
        separated = re.findall(
            VERSION_PATTERN,
            token,
            re.VERBOSE
        )

        for part in separated:
            if part.isdigit():
                parts.append(int(part))
            elif self._ishex(part) and len(part) >= 6:
                parts.append(int(part, 16))
            else:
                parts.append(part)

        return parts

    def _validation(self) -> None:
        self._key = (
            self.epoch,
            tuple(self._separate_and_classify(self.version)),
            tuple(self._separate_and_classify(self.release))
        )

    def __repr__(self):
        return f"{self.version}-{self.release}"
    
    def __hash__(self) -> int:
        return hash(self._key)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._key < other._key

    def __le__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._key <= other._key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._key == other._key

    def __ge__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._key >= other._key

    def __gt__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._key > other._key

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._key != other._key
