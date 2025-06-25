from pydantic import BaseModel
from typing import NamedTuple
from enum import Enum

class BranchName(Enum):
    """Contains branch names"""
    p11 = "p11"
    sisyphus = "sisyphus"

class Version(NamedTuple):
    version: str
    release: str

class PackageInfo(BaseModel):
    name: str
    epoch: int
    version: str
    release: str
    arch: str
    disttag: str
    buildtime: int
    source: str

class BranchBinaryPackages(BaseModel):
    length: int
    packages: list[PackageInfo]