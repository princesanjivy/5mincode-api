import json
import sys
from io import StringIO

from pydantic import BaseModel


class Test(BaseModel):
    input: str
    output: str


class TestCase(BaseModel):
    tests: list[Test]
    description: str


def execute_code_with_input(testcase):
    result = []

    with open("code.txt", "r") as fp:
        code = fp.read()

    original_stdin = sys.stdin
    original_stdout = sys.stdout

    for test in testcase.tests:
        fake_stdin = StringIO(test.input)

        try:
            sys.stdin = fake_stdin
            sys.stdout = StringIO()

            compiled_code = compile(code, "<string>", "exec")
            exec(compiled_code)

            printed_content = sys.stdout.getvalue()
            sys.stdout = original_stdout

            # assert printed_content == test.output
            if printed_content.strip() == test.output:
                print(f"Captured Output: {printed_content.strip()} | Passed")
                result.append(f"Captured Output: {printed_content.strip()} | Passed")
            else:
                print(
                    f"Captured Output: {printed_content.strip()} | Expected: {test.output} | Failed"
                )
                result.append(
                    f"Captured Output: {printed_content.strip()} | Expected: {test.output} | Failed"
                )
        except Exception as e:
            sys.stdout = original_stdout
            print(f"Caputred Error: {e} | Failed")
            result.append(f"Caputred Error: {e} | Failed")
        finally:
            sys.stdin = original_stdin
            # sys.stdout = original_stdout

    return result


with open("testcase.json", "r") as fp:
    tc = json.load(fp)

testcase = TestCase(**tc)


def run():
    print("exec started...")
    return execute_code_with_input(testcase)
