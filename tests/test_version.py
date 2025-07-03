import pytest
from core.version import Version


@pytest.mark.parametrize("epoch,version,release",[
    (0, "24.09", "alt2"),
    (0, "4.5.0.1.gitc003169", "alt1"),
    (0, "0.1.0", "alt7.git.82cae578"),
    (0, "2.1.3", "alt1.svn20140424"),
    (0, "3.0.1.20211001", "alt2"),
    (0, "2.3.0", "alt3.20200519"),
    (0, "3.0.6", "alt3.1.qa1"),
    (0, "1.2.1", "alt3.gd0e5d85"),
    (0, "7.0.5", "alt1.p3.2"),
    (0, "1.0.4", "alt3_5.hg653"),
    (0, "0.1.0", "alt4.hg20140818"),
    (0, "06032023", "alt1"),
    (0, "2.3.1.0.20.d265", "alt1"),
    (0, "0.108.0", "alt1.beta60"),
    (0, "0.2.2", "alt9.git8787e95"),
    (0, "0", "alt2_22.20200705.2a7d4a2"),
    (0, "20221019.0.70cb339f", "alt1"),
    (0, "1.0.6", "alt2.git.c02babd"),
    (0, "3.4", "alt2_3jpp11"),
    (0, "2.7.7", "alt12_67jpp11"),
    (0, "0.5.15lorg2", "alt96"),
    (0, "5.8", "alt1_13.arduino11"),
    (0, "git.20240126.e9a21c4", "alt1"),
    (0, "v2023.03", "alt1"),
    (0, "1.7.5+wayland2", "alt1")
])
def test_version_validate(epoch, version, release):
    version = Version(epoch, version, release)
    assert isinstance(version, Version)

@pytest.mark.parametrize("v1,v2,is_greater",[
    (
        (0, "0.2.2", "alt1"),    
        (1, "0.2.2", "alt1"),
        False
    ),
    (
        (0, "0.2.2", "alt1"),    
        (0, "0.4.9", "alt1"),
        False
    ),
    (
        (0, "0.2.2", "alt1"),    
        (0, "0.2.2", "alt2"),
        False
    ),
    (
        (0, "0.15", "alt1"),    
        (0, "0.9.4", "alt1"),
        True
    ),
    (
        (0, "0", "alt1.git.89f05ca"),    
        (0, "0", "alt1.git.7525914"),
        True
    ),
])
def is_greater_than(v1: str, v2: str, is_greater: bool):
    v1_obj = Version(*v1)
    v2_obj = Version(*v2)

    assert v1_obj > v2_obj == is_greater
