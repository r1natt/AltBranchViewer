import pytest
from core.compare import compare_branches, compare_versions
from core._types import BranchBinaryPackages, PackageInfo
from typing import List


def make_pkg(name, arch, version="version", release="release"):
    return PackageInfo(
        name=name,
        epoch=0,
        version=version,
        release=release,
        arch=arch,
        disttag="tag",
        buildtime=0,
        source="source"
    )

def make_bbp(packages_list: List[PackageInfo]):
    return BranchBinaryPackages.model_validate(
        {
            "length": len(packages_list),
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

@pytest.mark.parametrize("target_branch_packages,base_branch_packages,expected_compare_list",[
    (
        make_bbp([
            make_pkg("python", "x86_64", version="1", release="alt1"),
            make_pkg("torch", "x86_64", version="2", release="alt1"),
            make_pkg("python", "aarch64", version="3", release="alt1"),
            make_pkg("du", "aarch64", version="1", release="alt1")
        ]),
        make_bbp([
            make_pkg("python", "x86_64", version="1", release="alt5"),
            make_pkg("torch", "x86_64", version="1", release="alt1"),
            make_pkg("python", "aarch64", version="3", release="alt1"),
            make_pkg("du", "aarch64", version="3", release="alt1")
        ]),
        {"x86_64": ["python 1-alt5"], "aarch64": ["du 3-alt1"]}
    )
])
def test_compare_versions(target_branch_packages, 
                          base_branch_packages, 
                          expected_compare_list):
    
    compare_list = compare_versions(target_branch_packages, base_branch_packages)
    print(compare_list)
    assert compare_list == expected_compare_list
