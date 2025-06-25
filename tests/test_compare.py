import pytest
from core.compare import compare_branches, compare_versions, validate_version
from core._types import BranchBinaryPackages, PackageInfo, Version
from typing import List


def make_pkg(name, arch, version="version"):
    return PackageInfo(
        name=name,
        epoch=0,
        version=version,
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

@pytest.mark.parametrize("target_branch_packages,base_branch_packages,expected_compare_list",[
    (
        make_bbp([
            make_pkg("python", "x86_64", version="1-alt1"),
            make_pkg("torch", "x86_64", version="2-alt1"),
            make_pkg("python", "aarch64", version="3-alt1"),
            make_pkg("du", "aarch64", version="1-alt1")
        ]),
        make_bbp([
            make_pkg("python", "x86_64", version="1-alt5"),
            make_pkg("torch", "x86_64", version="1-alt1"),
            make_pkg("python", "aarch64", version="3-alt1"),
            make_pkg("du", "aarch64", version="3-alt1")
        ]),
        ["python", "du"]
    )
])
def test_compare_versions(target_branch_packages, 
                          base_branch_packages, 
                          expected_compare_list):
    
    compare_list = compare_versions(target_branch_packages, base_branch_packages)
    assert compare_list == expected_compare_list

@pytest.mark.parametrize("version_str",[
    ("24.09-alt2"),
    ("4.5.0.1.gitc003169-alt1"),
    ("0.1.0-alt7.git.82cae578"),
    ("2.1.3-alt1.svn20140424"),
    ("3.0.1.20211001-alt2"),
    ("2.3.0-alt3.20200519"),
    ("3.0.6-alt3.1.qa1"),
    ("1.2.1-alt3.gd0e5d85"),
    ("7.0.5-alt1.p3.2"),
    ("1.0.4-alt3_5.hg653"),
    ("0.1.0-alt4.hg20140818"),
    ("06032023-alt1"),
    ("2.3.1.0.20.d265-alt1"),
    ("0.108.0-alt1.beta60"),
    ("0.2.2-alt9.git8787e95"),
    ("0-alt2_22.20200705.2a7d4a2"),
    ("20221019.0.70cb339f-alt1"),
    ("1.0.6-alt2.git.c02babd"),
    ("3.4-alt2_3jpp11"),
    ("2.7.7-alt12_67jpp11"),
    ("0.5.15lorg2-alt96"),
    ("5.8-alt1_13.arduino11"),
    ("git.20240126.e9a21c4-alt1"),
    ("v2023.03-alt1"),
    ("1.7.5+wayland2-alt1")
])
def test_version_validate(version_str):
    version = validate_version(version_str)
    assert isinstance(version, Version)

