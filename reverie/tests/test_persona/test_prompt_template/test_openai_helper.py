import pytest
from loguru import logger

from backend_server.persona.prompt_template.openai_helper import get_caller_function_name, log_function_call

# Test case for get_caller_function_name
def test_get_caller_function_name():
    def dummy_function():
        return get_caller_function_name(r"dummy_fun.*")

    result = dummy_function()
    # result += ","

    assert result == "dummy_function", f"Expected 'dummy_function', but got {result}"

# Test case for log_function_call
def test_log_function_call(capfd):
    @log_function_call
    def sample_function(x, y):
        return x + y

    @log_function_call
    def run_gpt_sample_function(x, y):
        return x * y

    # Test the normal function call logging
    sample_function(1, 2)
    out, err = capfd.readouterr()
    assert "'input': {'args': (1, 2), 'kwargs': {}}" in out, out  # 使用 [1, 2] 代替 (1, 2)
    assert "'output': 3" in out, "Output not logged correctly."
    assert "'caller': None" in out, "Caller not logged correctly."

    # Test the function call with caller pattern match
    run_gpt_sample_function(3, 4)
    out, err = capfd.readouterr()
    assert "'input': {'args': (3, 4), 'kwargs': {}}" in out, "Input not logged correctly."
    assert "'output': 12" in out, "Output not logged correctly."
    # assert 'run_gpt_sample_function' in out, "Caller not logged correctly."


if __name__ == "__main__":
    pytest.main()
