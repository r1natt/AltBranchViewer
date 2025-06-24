import pytest
from core import RepoHandler, BranchName


@pytest.mark.parametrize("branch_name,output",[
    ("p11", BranchName.p11),
])
def test_branch_name_validation_correct(branch_name, output):
    rh = RepoHandler()
    result = rh._validate_branch_name(branch_name)
    assert result == output

@pytest.mark.parametrize("invalid_branch_name",[
    (1),
    (-1.2),
    (True)
])
def test_branch_name_validation_type_error(invalid_branch_name):
    rh = RepoHandler()
    with pytest.raises(TypeError):
        rh._validate_branch_name(invalid_branch_name)

@pytest.mark.parametrize("invalid_branch_name",[
    ("pp11"),
    ("asdf"),
])
def test_branch_name_validation_value_error(invalid_branch_name):
    rh = RepoHandler()
    with pytest.raises(ValueError):
        rh._validate_branch_name(invalid_branch_name)
