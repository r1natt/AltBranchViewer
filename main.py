from pprint import pprint

from core.api import get_branch_binary_packages
from core.compare import compare_branches



def main():
    p11_bp = get_branch_binary_packages("p11")
    sisyphus_bp = get_branch_binary_packages("sisyphus")
    print("get packages")

    print(len(p11_bp.packages))

    in_target, in_base = compare_branches(p11_bp, sisyphus_bp)

    list_len = 0
    for arch, packages in in_target.items():
        list_len += len(packages)
    print(list_len)

    list_len = 0
    for arch, packages in in_base.items():
        list_len += len(packages)
    print(list_len)

main()