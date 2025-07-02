import json
import requests
from core._types import BranchBinaryPackages, BranchName
from logger import logger
from typing import Union

API_URL = "https://rdb.altlinux.org/api"

def get_branch_binary_packages(branch_name: BranchName) -> Union[BranchBinaryPackages, None]:
    """Api request to /export/branch_binry_packages/{branch_name}"""
    try:
        endpoint = API_URL + "/export/branch_binary_packages/" + branch_name.value

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
