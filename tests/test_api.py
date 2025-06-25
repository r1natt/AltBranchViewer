import pytest
from core.api import get_branch_binary_packages, validate_branch_name, BranchName


@pytest.mark.parametrize("branch_name,output",[
    ("p11", BranchName.p11),
])
def test_branch_name_validation_correct(branch_name, output):
    result = validate_branch_name(branch_name)
    assert result == output

@pytest.mark.parametrize("invalid_branch_name",[
    (1),
    (-1.2),
    (True)
])
def test_branch_name_validation_type_error(invalid_branch_name):
    with pytest.raises(TypeError):
        validate_branch_name(invalid_branch_name)

@pytest.mark.parametrize("invalid_branch_name",[
    ("pp11"),
    ("asdf"),
])
def test_branch_name_validation_value_error(invalid_branch_name):
    with pytest.raises(ValueError):
        validate_branch_name(invalid_branch_name)
