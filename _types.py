from pydantic import BaseModel


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