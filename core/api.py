import json
import requests
from requests.exceptions import HTTPError
import traceback
from core._types import BranchBinaryPackages, BranchName
from logger import logger

API_URL = "https://rdb.altlinux.org/api"

def validate_branch_name(branch_name: str) -> BranchName:
    if not(isinstance(branch_name, str)):
        raise TypeError("Branch name must be str or BranchName")
    try:
        return BranchName(branch_name)
    except ValueError:
        raise ValueError(f"Wrong branch name: {branch_name}. Correct names: {', '.join([bn.value for bn in BranchName])}")

def get_branch_binary_packages(branch_name: str) -> BranchBinaryPackages | None:
    """Api request to /export/branch_binry_packages/{branch_name}"""
    try:
        validated_branch_name = validate_branch_name(branch_name)

        endpoint = API_URL + "/export/branch_binary_packages/" + validated_branch_name.value

        branch_binary_packages = requests.get(endpoint)
        branch_binary_packages.raise_for_status()

        if branch_binary_packages.status_code != 200:
            logger.error(f"Error during api requests: {branch_binary_packages.status_code} error code")
        else:
            branch_binary_packages_json = json.loads(branch_binary_packages.text)

            return BranchBinaryPackages.model_validate(branch_binary_packages_json)
    except Exception as e:
        logger.critical(f"Error during api requests: {e}")
        raise e