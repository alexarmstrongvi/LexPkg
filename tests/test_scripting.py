# Standard library
from pathlib import Path
import copy
import shutil

# 3rd party
import pytest

# Local
from lexpkg.scripting import (
    update_config,
    require_empty_dir,
)

################################################################################
def test_update_config():

    # Value update 
    original = {'A' : 1, 'B' : 2}
    update   = {'A' : 9}
    result   = {'A' : 9, 'B' : 2}
    assert update_config(original, update) == result
    
    # Original input not mutated by default but copying can be disabled
    original = {'A' : 1, 'B' : 2}
    update   = {'A' : 2}
    original_deepcopy = copy.deepcopy(original)
    combined = update_config(original, update)
    assert original == original_deepcopy
    assert original is not combined
    combined = update_config(original, update, copy=False)
    assert original != original_deepcopy
    assert original is combined
    
    # Sub-dictionary update 
    original = {
        'A' : 1,
        'B' : {'X' : 2, 'Y' : 3},
    }
    update = {
        'B' : {'X' : 9},
    }
    result = {
        'A' : 1,
        'B' : {'X' : 9, 'Y' : 3},
    }
    assert update_config(original, update) == result
    
    # Sub-list update 
    original = {'A' : [2,3]}
    update   = {'A' : [2,1]}
    # Append only new elements by default
    assert update_config(original, update)['A'] == [2,3,1]
    # Enable concatenation of lists, allowing for duplicates 
    assert update_config(original, update, concat_lists=True)['A'] == [2,3,2,1]
    # Enable simple overwriting of lists
    assert update_config(original, update, overwrite_lists=True)['A'] == [2,1]

    # New keys not allowed by default but can be explicitely allowed
    original = {'A' : 1}
    update   = {'Z' : 1}
    with pytest.raises(KeyError):
        update_config(original, update)
    update_config(original, update, allow_new_keys=True)

    # Edge cases
    config = {'A' : 1}
    assert update_config(config, {}) == config
    assert update_config({}, config, allow_new_keys=True) == config
    config = {'A' : None}
    update = {'A' : {'X' : 1}}
    assert update_config(config, update) == update
    config = {'A' : None}
    update = {'A' : [1,2]}
    assert update_config(config, update) == update

def test_require_empty_dir(monkeypatch):
    empty_dir = Path('path_to/empty_dir')

    assert not empty_dir.parent.is_dir()

    # Error if parent directory does not exist by default
    with pytest.raises(FileNotFoundError):
        require_empty_dir(empty_dir)
    require_empty_dir(empty_dir, parents=True)
    assert empty_dir.is_dir()

    # Do nothing if directory exists but is empty
    require_empty_dir(empty_dir)
    assert empty_dir.is_dir()

    # Error if directory exists and is not empty
    (empty_dir/'file.txt').write_text('TEST\n')
    with monkeypatch.context() as m:
        with pytest.raises(FileExistsError):
            m.setattr('lexpkg.user_input.request_permission', lambda _ : False)
            require_empty_dir(empty_dir)
        # User can choose to remove output directory
        m.setattr('lexpkg.user_input.request_permission', lambda _ : True)
        require_empty_dir(empty_dir)

    shutil.rmtree(empty_dir.parent)
