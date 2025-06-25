from pprint import pprint

from logger import logger
from core.api import get_branch_binary_packages
from core.compare import compare_branches



def main():
    p11_bp = get_branch_binary_packages("p11")
    logger.info(f"get p11 packages ({p11_bp.length} packages)")
    sisyphus_bp = get_branch_binary_packages("sisyphus")
    logger.info(f"get sisyphus packages ({sisyphus_bp.length} packages)")

    in_target, in_base = compare_branches(p11_bp, sisyphus_bp)

    list_len = 0
    for arch, packages in in_target.items():
        list_len += len(packages)
    logger.info(f"{list_len} unique packages in target")

    list_len = 0
    for arch, packages in in_base.items():
        list_len += len(packages)
    logger.info(f"{list_len} unique packages in base")


main()