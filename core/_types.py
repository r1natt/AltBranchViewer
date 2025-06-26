from pydantic import BaseModel
from typing import NamedTuple
from enum import Enum

class BranchName(Enum):
    """Contains branch names"""
    sisyphus="sisyphus"
    sisyphus_e2k="sisyphus_e2k"
    sisyphus_riscv64="sisyphus_riscv64"
    sisyphus_loongarch64="sisyphus_loongarch64"
    p11="p11"
    p10="p10"
    p10_e2k="p10_e2k"
    p9="p9"
    c10f2="c10f2"
    c9f2="c9f2"

def validate_branch_name(branch_name: str) -> BranchName:
    if not(isinstance(branch_name, str)):
        raise TypeError("Branch name must be str or BranchName")
    try:
        return BranchName(branch_name)
    except ValueError:
        raise ValueError(f"Wrong branch name: {branch_name}. Correct names: {', '.join([bn.value for bn in BranchName])}")

class Version(NamedTuple):
    version: str
    release: str

    def __str__(self):
        return f"{self.version}-{self.release}"

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