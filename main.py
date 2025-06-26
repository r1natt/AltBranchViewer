from pprint import pprint

from logger import logger
from core.api import get_branch_binary_packages
from core.compare import compare_branches, compare_versions
from core._types import BranchBinaryPackages, validate_branch_name
import argparse
import json
from enum import Enum


class Actions(Enum):
    compare_all = "compare_all"
    compare_branches = "compare_branches"
    compare_versions = "compare_versions"


def argparser():
    parser = argparse.ArgumentParser(
        prog='AltLinux Repo Manager',
        description='Print unique packages in input branches. Compare versions in input branches',
        epilog='Text at the bottom of help'
    )

    parser.add_argument("-f", "--output-filename")

    subparsers = parser.add_subparsers(
        dest="action",
        required=True,
        help="Action to perform (choose one)"
    )

    parser_compare = subparsers.add_parser(Actions.compare_all.value, help="Full comparison")
    parser_compare.add_argument("target")
    parser_compare.add_argument("base")

    parser_cb = subparsers.add_parser(Actions.compare_branches.value, help="Compare package names")
    parser_cb.add_argument("target")
    parser_cb.add_argument("base")

    parser_cv = subparsers.add_parser(Actions.compare_versions.value, help="Compare package versions")
    parser_cv.add_argument("target")
    parser_cv.add_argument("base")

    return parser.parse_args()

def make_request(branch_name) -> BranchBinaryPackages:
    repo_packages = get_branch_binary_packages(branch_name)
    logger.info(f"get {branch_name} packages ({repo_packages.length} packages)")
    return repo_packages

def make_comparing(target_branch_name, base_branch_name, action):
    target_branch_packages = make_request(target_branch_name)
    base_branch_packages = make_request(base_branch_name)

    return_dict = {}

    if action == Actions.compare_all.value \
        or action == Actions.compare_branches.value:
        unique_in_target, unique_in_base = compare_branches(target_branch_packages, base_branch_packages)
        for arch_name in unique_in_target.keys():
            return_dict[arch_name] = {
                "unique_in_target": unique_in_target[arch_name],
                "unique_in_base": unique_in_base[arch_name]
            }
    if action == Actions.compare_all.value \
        or action == Actions.compare_versions.value:
        newer_in_base = compare_versions(target_branch_packages, base_branch_packages)

        for arch_name in newer_in_base.keys():
            if arch_name not in return_dict:
                return_dict[arch_name] = {
                    f"newer_in_base": newer_in_base[arch_name]
                }
            else:
                return_dict[arch_name][f"newer_in_bases"] = newer_in_base[arch_name]
    return return_dict

def save_to_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file)

def main():
    args = argparser()

    target_branch_name, base_branch_name = validate_branch_name(args.target), validate_branch_name(args.base)

    comparing_result = make_comparing(target_branch_name, base_branch_name, args.action)

    filename = "output.json"
    if args.output_filename is not None:
        filename = args.output_filename

    save_to_file(filename, comparing_result)
    logger.info(f"result save in {filename}")
    

if __name__ == "__main__":
    main()