 This project is a test task.

# :clipboard: Description

🐍Python3.9+ Support

This project is a cli utility that addresses https://rdb.altlinux.org/api and can compare packages in two branches (`target` and `base`) according to criteria:

* Outputs unique packages that are on one branch, but which are not in the second.
* Outputs which packages in the `base` branch are newer (latest version) than those on the `target` branch.

The script calls the `/export/branch_binary_packages/{branch}` method, where branch is the name of the repository branch.

__Important note: the result of API execution `/export/branch_binary_packages/{branch}`, includes an indication of the architecture for which the package was compiled. As a result of the script, I also output the answer for different architectures.__

# :sparkles: Installation

1. Clone repository
```bash
git clone https://github.com/r1natt/AltBranchViewer.git
```
2. Change dir to repo folder
```bash
cd AltBranchViewer
```
3. Make Pyenv and install requirements
```bash
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

# :pencil2: Usage

* **Compare and versions and branches**

```bash
python main.py compare_all <target_branch_name> <base_branch_name>
```

* **Compare only branches**

```bash
python main.py compare_branches <target_branch_name> <base_branch_name>
```

* **Compare only versions**

```bash
python main.py compare_versions <target_branch_name> <base_branch_name>
```

* **Output in specify file**

✅Correct option

```bash
python main.py -f filename.json compare_versions <target_branch_name> <base_branch_name>
```

❌This is not working

```bash
python main.py compare_versions <target_branch_name> <base_branch_name> -f filename.json
```

# :bulb: Examples

* **Compare Branches**

```bash
python main.py compare_branches p11 sisyphus
```

Output:

```json
{
    "aarch64": {
        "unique_in_target": ["ghc9.2-unix-debuginfo", "x2x", "ghc9.0-directory-debuginfo"],
        "unique_in_base": ["inlyne", "libyui-qt-devel", "dqt5-webengine-devel-debuginfo"]
    },
    "i586": {
        "unique_in_target": ["ghc9.2-unix-debuginfo", "x2x", "ghc9.0-directory-debuginfo"],
        "unique_in_base": ["inlyne", "libyui-qt-devel", "dqt5-webengine-devel-debuginfo"]
    }
}
```

---

* **Compare versions**

```bash
python main.py compare_versions p11 sisyphus
```

Output:

```json
{
    "aarch64": {
        "newer_in_base": ["3proxy 0.6.1-2", "3proxy-debuginfo 0.6.1-2", "7colors 0.10-1"]
    },
    "i586": {
        "newer_in_base": ["3proxy 0.6.1-2", "3proxy-debuginfo 0.6.1-2", "7colors 0.10-1"]
    }
}
```

---

* **Compare all**

Execute both compare_branches and compare_versions funcs

```bash
python main.py compare_all p11 sisyphus
```

Output:

```json
{
    "aarch64": {
        "newer_in_base": ["3proxy 0.6.1-2", "3proxy-debuginfo 0.6.1-2", "7colors 0.10-1"],
        "unique_in_target": ["ghc9.2-unix-debuginfo", "x2x", "ghc9.0-directory-debuginfo"],
        "unique_in_base": ["inlyne", "libyui-qt-devel", "dqt5-webengine-devel-debuginfo"]
    },
    "i586": {
        "newer_in_base": ["3proxy 0.6.1-2", "3proxy-debuginfo 0.6.1-2", "7colors 0.10-1"],
        "unique_in_target": ["ghc9.2-unix-debuginfo", "x2x", "ghc9.0-directory-debuginfo"],
        "unique_in_base": ["inlyne", "libyui-qt-devel", "dqt5-webengine-devel-debuginfo"]
    }
}
```

* **Output in specify file**

Execute both compare_branches and compare_versions funcs

```bash
python main.py -f p11_sisyphus.json compare_all p11 sisyphus
```

Output:

```json
{
    "aarch64": {
        "newer_in_base": ["3proxy 0.6.1-2", "3proxy-debuginfo 0.6.1-2", "7colors 0.10-1"],
        "unique_in_target": ["ghc9.2-unix-debuginfo", "x2x", "ghc9.0-directory-debuginfo"],
        "unique_in_base": ["inlyne", "libyui-qt-devel", "dqt5-webengine-devel-debuginfo"]
    },
    "i586": {
        "newer_in_base": ["3proxy 0.6.1-2", "3proxy-debuginfo 0.6.1-2", "7colors 0.10-1"],
        "unique_in_target": ["ghc9.2-unix-debuginfo", "x2x", "ghc9.0-directory-debuginfo"],
        "unique_in_base": ["inlyne", "libyui-qt-devel", "dqt5-webengine-devel-debuginfo"]
    }
}
```
