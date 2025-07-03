from typing import Tuple, Union
import re


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
    
    def _classify_token(self, token):
        results = []

        match = re.fullmatch(r'(git|hg|g)?([a-fA-F0-9]{6,})', token)
        if match:
            prefix, hex_part = match.groups()
            if prefix:
                results.append(prefix) # str
            results.append(hex_part) # hex
            return results

        if re.fullmatch(r'[a-fA-F0-9]', token):
            return token # str

        if re.fullmatch(r'\d+', token):
            return int(token) # int

        if re.fullmatch(r'[a-zA-Z][\w\d]*', token):
            return token # word

        return [('unknown', token)]

    def _validation(self):
        """
        Должен осуществлять проверку на
        буквенные значения
        цифры
        hex значения
        """
        version_parts = re.split(r'[.\-_+]', self.version)
        validated_version = [self._classify_token(part) for part in version_parts if part]

        release_parts = re.split(r'[.\-_+]', self.release)
        validated_release = [self._classify_token(part) for part in release_parts if part]

        self.key = (
            self.epoch,
            tuple(validated_version),
            tuple(validated_release)
        )

# Пример
versions = [
    ("24.09", "alt2"),
    ("4.5.0.1.gitc003169", "alt1"),
    ("0.1.0", "alt7.git.82cae578"),
    ("2.1.3", "alt1.svn20140424"),
    ("3.0.1.20211001", "alt2"),
    ("2.3.0", "alt3.20200519"),
    ("3.0.6", "alt3.1.qa1"),
    ("1.2.1", "alt3.gd0e5d85"),
    ("7.0.5", "alt1.p3.2"),
    ("1.0.4", "alt3_5.hg653"),
    ("0.1.0", "alt4.hg20140818"),
    ("06032023", "alt1"),
    ("2.3.1.0.20.d265", "alt1"),
    ("0.108.0", "alt1.beta60"),
    ("0.2.2", "alt9.git8787e95"),
    ("0", "alt2_22.20200705.2a7d4a2"),
    ("20221019.0.70cb339f", "alt1"),
    ("1.0.6", "alt2.git.c02babd"),
    ("3.4", "alt2_3jpp11"),
    ("2.7.7", "alt12_67jpp11"),
    ("0.5.15lorg2", "alt96"),
    ("5.8", "alt1_13.arduino11"),
    ("git.20240126.e9a21c4", "alt1"),
    ("v2023.03", "alt1"),
    ("1.7.5+wayland2", "alt1")
]

for version in versions:
    print(f"\n{version}:")
    v = Version(0, version[0], version[1])
    print(v.key)
