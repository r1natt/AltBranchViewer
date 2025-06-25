import pytest
from core.compare import compare_branches
from core._types import BranchBinaryPackages, PackageInfo
from typing import List


def make_pkg(name, arch):
    return PackageInfo(
        name=name,
        epoch=0,
        version="version",
        release="release",
        arch=arch,
        disttag="tag",
        buildtime=0,
        source="source"
    )

def make_bbp(packages_list: List[PackageInfo]):
    return BranchBinaryPackages.model_validate(
        {
            "length": 4,
            "packages": packages_list
        }
    )

@pytest.mark.parametrize("target_branch_packages,base_branch_packages,target_unique,base_unique",[
    (
        make_bbp([
            make_pkg("python", "x86_64"),
            make_pkg("torch", "x86_64"),
            make_pkg("python", "aarch64"),
            make_pkg("du", "aarch64")
        ]),
        make_bbp([
            make_pkg("python", "x86_64"),
            make_pkg("tenserflow", "x86_64"),
            make_pkg("python", "aarch64"),
            make_pkg("df", "aarch64")
        ]),
        {"x86_64": ["torch"], "aarch64": ["du"]},
        {"x86_64": ["tenserflow"], "aarch64": ["df"]}
    )
])
def test_compare_branches(target_branch_packages, 
                          base_branch_packages, 
                          target_unique, 
                          base_unique):
    in_target, in_base = compare_branches(target_branch_packages, base_branch_packages)

    print(in_target, in_base)
    assert in_target == target_unique
    assert in_base == base_unique
    