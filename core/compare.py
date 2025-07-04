from core._types import BranchBinaryPackages, PackageInfo
from typing import List, Dict, Set
from core.version import Version
import traceback
from logger import logger


def arch_separation(packages: List[PackageInfo]) -> Dict[str, Set[str]]:
    """Returns dict, key is arch name, value is list of packages that arch"""
    arch_packages = {}

    for package in packages:
        if package.arch not in arch_packages.keys():
            arch_packages[package.arch] = set()
        arch_packages[package.arch].add(package.name)
    return arch_packages

def compare_branches(
        target_branch_packages: BranchBinaryPackages, 
        base_branch_packages: BranchBinaryPackages) -> Dict[str, List[str]]:
    """Print package names of target_branch and not in base_branch"""

    target_arch_separated = arch_separation(target_branch_packages.packages)
    base_arch_separated = arch_separation(base_branch_packages.packages)
    # target_arch_separated, base_arch_separated - словари, ключами которых являются 
    # названия арзитектур, то я сравниваю пакеты каждой архитектуры отдельно

    only_in_target = {arch_name:[] for arch_name in target_arch_separated}
    only_in_base = {arch_name:[] for arch_name in base_arch_separated}

    # Чтобы не проходится по спискам пакетов 2 раза: для target и base по 
    # отдельности, я прохожусь циклом только по target.
    # Я сохраняю в only_in_target пакеты, которые есть только в target, а те 
    # пакеты, которые повторяются я удаляю из base_arch_separated, то есть после 
    # работы цикла в base_arch_separated останутся уникальные для base пакеты
    for arch, packages_set in target_arch_separated.items():
        for package_name in packages_set:
            if package_name not in base_arch_separated[arch]:
                only_in_target[arch].append(package_name)
            else:
                base_arch_separated[arch].remove(package_name)
        only_in_base[arch] = list(base_arch_separated[arch])

    return only_in_target, only_in_base

def arch_separation_with_version(branch_packages: BranchBinaryPackages) -> Dict[str, Dict[str, Version]]:
    """Like arch_separation, but instead of set of packages, value is Dict[str, Version]"""
    arch_packages = {}

    for package in branch_packages.packages:
        if package.arch not in arch_packages.keys():
            arch_packages[package.arch] = {}
        arch_packages[package.arch][package.name] = Version(
            package.epoch, 
            package.version, 
            package.release
        )
    return arch_packages

def compare_versions(
        target_branch_packages: BranchBinaryPackages, 
        base_branch_packages: BranchBinaryPackages) -> List[str]:
    """Return list, contains packages newer in base than in target branches"""
    
    return_dict = {}

    separeted_target_packages = arch_separation_with_version(target_branch_packages)
    separeted_base_packages = arch_separation_with_version(base_branch_packages)

    for arch_name, packages_version in separeted_target_packages.items():
        for name, version in packages_version.items():
            if arch_name in separeted_base_packages.keys() and name in separeted_base_packages[arch_name]:
                t_pack_ver = version
                b_pack_ver = separeted_base_packages[arch_name][name]

                if arch_name not in return_dict:
                    return_dict[arch_name] = []

                if b_pack_ver > t_pack_ver:
                    return_dict[arch_name].append(f"{name} {b_pack_ver}")
    return return_dict
