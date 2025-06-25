from core._types import BranchBinaryPackages, PackageInfo
from typing import List, Dict, TypeAlias

arch: TypeAlias = str

def arch_separation(packages: List[PackageInfo]) -> Dict[arch, List[PackageInfo]]:
    """Returns dict, key is arch name, value is list of packages that arch"""
    arch_packages = {}

    for package in packages:
        if package.arch not in arch_packages.keys():
            arch_packages[package.arch] = set()
        arch_packages[package.arch].add(package.name)
    return arch_packages

def compare_branches(
        target_branch_packages: BranchBinaryPackages, 
        base_branch_packages: BranchBinaryPackages) -> Dict[arch, List[str]]:
    """Print package names of target_branch and not in base_branch"""

    target_separated = arch_separation(target_branch_packages.packages)
    base_separated = arch_separation(base_branch_packages.packages)
    # target_separated, base_separated - словари, ключами которых являются 
    # названия арзитектур, то я сравниваю пакеты каждой архитектуры отдельно

    only_in_target = {arch_name:[] for arch_name in target_separated}
    only_in_base = {arch_name:[] for arch_name in base_separated}

    # Чтобы не проходится по спискам пакетов 2 раза: для target и base по 
    # отдельности, я прохожусь циклом только по target.
    # Я сохраняю в only_in_target пакеты, которые есть только в target, а те 
    # пакеты, которые повторяются я удаляю из base_separated, то есть после 
    # работы цикла в base_separated останутся уникальные для base пакеты
    for arch, packages_list in target_separated.items():
        for package in packages_list:
            if package not in base_separated[arch]:
                only_in_target[arch].append(package)
            else:
                base_separated[arch].remove(package)
        only_in_base[arch] = list(base_separated[arch])

    return only_in_target, only_in_base
