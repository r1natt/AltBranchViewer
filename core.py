from enum import Enum
import json
import requests
from pprint import pprint
from typing import Union
from _types import BranchBinaryPackages

ARCH = "x86_64"

class BranchName(Enum):
    """Contains branch names"""
    p11 = "p11"
    sisyphus = "sisyphus"

class RepoHandler:
    """Make requests to rdb.altlinux.org api"""
    def __init__(self):
        pass

    def _validate_branch_name(self, branch_name: Union[BranchName, str]) -> BranchName:
        if isinstance(branch_name, BranchName):
            return branch_name
        elif not(isinstance(branch_name, str)):
            raise TypeError("Branch name must be str or BranchName")
        try:
            return BranchName(branch_name)
        except ValueError:
            raise ValueError(f"Wrong branch name: {branch_name}. Correct names: {', '.join([bn.value for bn in BranchName])}")

    def getBranchBinaryPackages(self, branch_name: Union[BranchName, str]):
        validated_branch_name = self._validate_branch_name(branch_name)

        branch_binary_packages = requests.get(
            f'https://rdb.altlinux.org/api/export/branch_binary_packages/{validated_branch_name.value}',
            params={
                "arch": ARCH
            }
        )
        branch_binary_packages_list = json.loads(branch_binary_packages.text)

        print(BranchBinaryPackages.model_validate(branch_binary_packages_list))


class Compare():
    """Compare repos in different branches"""
    def __init__(self):
        pass


rh = RepoHandler()
rh.getBranchBinaryPackages("p11")