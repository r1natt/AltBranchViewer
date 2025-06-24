from enum import Enum
import json
import requests
import traceback
from core._types import BranchBinaryPackages

class BranchName(Enum):
    """Contains branch names"""
    p11 = "p11"
    sisyphus = "sisyphus"

def validate_branch_name(branch_name: str) -> BranchName:
    if not(isinstance(branch_name, str)):
        raise TypeError("Branch name must be str or BranchName")
    try:
        return BranchName(branch_name)
    except ValueError:
        raise ValueError(f"Wrong branch name: {branch_name}. Correct names: {', '.join([bn.value for bn in BranchName])}")

def get_branch_binary_packages(branch_name: str) -> BranchBinaryPackages | None:
    """Api request to /export/branch_binary_packages/{branch_name}"""
    try:
        validated_branch_name = validate_branch_name(branch_name)

        branch_binary_packages = requests.get(
            f'https://rdb.altlinux.org/api/export/branch_binary_packages/{validated_branch_name.value}')
        if branch_binary_packages.status_code != 200:
            print(f"Error during api requests: {branch_binary_packages.status_code} error code")
            return None
        else:
            branch_binary_packages_list = json.loads(branch_binary_packages.text)

            return BranchBinaryPackages.model_validate(branch_binary_packages_list)
    except Exception as e:
        print(traceback.format_exc())
        return None