from pprint import pprint

from logger import logger
from core.api import get_branch_binary_packages
from core.compare import compare_branches, compare_versions
import re
from typing import NamedTuple


def main():
    p11_bp = get_branch_binary_packages("p11")
    logger.info(f"get p11 packages ({p11_bp.length} packages)")

    sisyphus_bp = get_branch_binary_packages("sisyphus")
    logger.info(f"get sisyphus packages ({sisyphus_bp.length} packages)")

    unique_in_p11, unique_in_sisyphus = compare_branches(p11_bp, sisyphus_bp)
    newer_in_sisyphus = compare_versions(p11_bp, sisyphus_bp)

    return_dict = {}
    for arch_name in unique_in_p11.keys():
        return_dict[arch_name] = {
            "unique_in_p11": unique_in_p11[arch_name],
            "unique_in_sisyphus": unique_in_sisyphus[arch_name],
            "newer_in_sisyphus": unique_in_sisyphus[arch_name]
        }
    
    pprint(return_dict)



main()