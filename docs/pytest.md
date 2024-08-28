# Unit testing with pyTest

Unit tests are a crucial component of any well-maintained code repository. Not only do they ensure that your code 
functions correctly, but they also help you verify that your code continues to work as expected when you update or 
modify specific parts. This is especially important in the context of Continuous Integration/Continuous Delivery 
(CI/CD), where code is frequently updated — sometimes by other developers. Unit tests help ensure that these changes do 
not disrupt the core functionality of your work, enabling safe integration of new changes.

There are several additional benefits to writing unit tests:

 - __Promotes Modular Code Development__: Writing unit tests alongside your code encourages you to design your code in 
   a modular fashion, breaking it down into smaller, more manageable functions or methods that each handle a single 
   responsibility. This practice not only improves the quality of your code but also makes you a better developer over
   time. 
 - __Provides Usage Examples__: Unit tests serve as practical examples of how your code is intended to be used. This 
   can be beneficial not only for other developers who may work on the codebase but also for you when revisiting the 
   project after some time. 
 - __Highlights Performance Bottlenecks__: By regularly running unit tests, you can identify which parts of your code 
   are most resource-intensive, allowing you to focus on optimizing these areas in future development efforts. 
 - __Meets Industry Standards__: Many international coding standards, commercial organizations, and auditing bodies 
   view unit tests as a foundational element of safe and reliable software development. This is particularly critical 
   in fields like medical research, where code quality directly impacts safety and compliance.
 - __Catching Bugs Early__: Unit tests allow you to identify bugs and issues early in the development process, often 
   before the code is integrated with other parts of the system. This early detection reduces the cost and effort 
   required to fix issues compared to finding them later in the development cycle.
 - __Encourages Code Reuse__: Writing unit tests often encourages the development of smaller, more modular components,
   which are easier to reuse across different parts of the codebase or in other projects.
 - __Promotes Code Ownership__: In teams, unit tests help promote a sense of shared ownership of the code. When tests
   are in place, all team members can confidently make changes, knowing that the tests will help safeguard the 
   integrity of the codebase.


## What is a unit test?
A unit test is a piece of code (written by you) that tests that a particular function is working as you would expect it 
to. Typically, as input it will take some data, either pre-defined, simulated, or acquired, and for which you know what 
the output should be when given to your particular function. 

### Example of a testable unit of code
As an example, we have been asked to write a software function that accepts as input a weight in kilograms (kg) and 
converts it into pounds (lb). Let's assume that the conversion rate is (to 5 decimal places):
$$
1 \text{kg} = 2.20462 \text{lb}
$$
Our code might be something simple like
```python
def convert_kg_to_lb(weight_kg: float) -> float:
    """ Converts weight in kilograms to pounds (to 5.d.p)
    
    Assumes conversion of 1 kg = 2.20462 lb
    
    Args:
        weight_kg (float): The weight in kg.
        
    Returns:
        float: The weight in lb    
    """
    return round(weight_kg * 2.20462, 5)
```

### First unit test
In this case our unit test could be (typically written in a different python file):
```python
from module import convert_kg_to_lb  # Replace 'module' with actual name of the module where function is located

def test_convert_kg_to_lb():
    assert convert_kg_to_lb(1) == 2.20462, f"bad conversion for 1"  # Test a simple case
    assert convert_kg_to_lb(0) == 0, f"bad conversion for 0"  # Test zero
    assert convert_kg_to_lb(-1) == -2.20462, f"bad conversion for -1"  # Test negative weight
    assert convert_kg_to_lb(100) == 220.462, f"bad conversion for 100"  # Test a larger number
    assert convert_kg_to_lb(2.5) == 5.51155, f"bad conversion for 2.5"  # Test with a fractional weight
    assert convert_kg_to_lb(0.001) == 0.00220462, f"bad conversion for 0.001"  # Test with a very small weight
```
There are no rules as to what ranges of data you should try - this depends on the problem at hand and is up to you.

<a id="method_names"></a>
!!! note
    
    It is essential that the name of the test makes sense. It __must__ start with `test` in order for pyTest to 
    recognize it as one and run it. What follows should tell the reader which function you are going to test. There 
    is no sense in using names like `test1` or `test_a`, because it will be difficult to know which method this is 
    suposed to be testing. It is good practise to use `test_name_of_method` to make it clear. It also help to add a 
    docstring for the unit test method that helps the reader know what the test is suposed to achieve, but not essenital
    if the code is well written.

One thing you will notice straight away is the use of the keyword `assert`. This is just handy shorthand for the 
following, but much easier to read:
```python
if convert_kg_to_lb(1) != 2.20426:
    raise AssertionError("bad conversion for 1")
```

The important part is that when this error is encountered by a _test runner_ (PyTest in our case), this does not stop 
the rest of the tests from executing. It will simply record the failure and report it to you as part of the summary 
statistics on the tests at the end of the test run (of course you are aiming for no failures!).

!!! tip
    
    I have found that ChatGPT is quite good at developing a unit test for you - at least it can be a good place to 
    start. It is important that you go through all the tests and ensure they are doing what you expect and that they 
    cover the ranges of inputs/outputs you are expecting to see in your method, and handle exceptions gracefully.

### Testing for errors
In the example provided above, you will notice that we have explicitly allowed (and tested for) negative weights.
In reality, we would like to check that our function handles infeasible values gracefully. Here is a revised version of 
our code:

```python
def convert_kg_to_lb(weight_kg: float) -> float:
    """ Converts weight in kilograms to pounds
    
    Args:
        weight_kg (float): The weight in kg.
        
    Returns:
        float: The weight in lb    
        
    Raises:
        ValueError: When a negative weight is provided as input.
    """
    if weight_kg < 0:
        raise ValueError("weight_kg must be positive!")
    return weight_kg * 2.20462
```

The unit test should now explicitly test for this exception also:
```python
import pytest
from module import convert_kg_to_lb  # Replace 'your_module' with actual name of the module where function is located

def test_convert_kg_to_lb():
    assert convert_kg_to_lb(1) == pytest.approx(2.20462, abs=1e-6), f"bad conversion for 1"
    assert convert_kg_to_lb(0) == pytest.approx(0, abs=1e-6), f"bad conversion for 0" 
    assert convert_kg_to_lb(100) == pytest.approx(220.462, abs=1e-6), f"bad conversion for 100" 
    assert convert_kg_to_lb(2.5) == pytest.approx(5.51155, abs=1e-6), f"bad conversion for 2.5" 
    assert convert_kg_to_lb(0.001) == pytest.approx(0.00220462, abs=1e-6), f"bad conversion for 0.001"

def test_convert_kg_to_lb_negative_value():
    # Test that a negative weight raises a ValueError with the correct message returned.
    with pytest.raises(ValueError, match="weight_kg must be positive!"):
        convert_kg_to_lb(-1)
```
Not only does this check that the right _kind_ of error is raise, but that the error message is correct (via the 
`match` keyword).  

### Testing approximations
Notice that in the above we have also introduces the `pytest.approx` method. This is useful when comparing 
floating-point numbers which may not be identical due to machine precision. You just need to specify how close they 
should be (via the `abs` keyword). Here we have settled for `abs=1e-6` as our method returns values to 5.d.p. This is 
useful because if we were to update the implementation of `convert_kg_to_lb` method to use a more precise conversion of
`1 kg = 2.2046226218488 lb`, these tests would still pass, confirming the change did not break anything. 

!!! note
    
    If we extended the accuracy of the _returned_ value from `convert_kg_to_lb`, say to 8 decimal places, this would 
    require us to redefine the precision of our unit tests (`abs=1e-9` for example). Also, we should inform our users 
    that the change is going to occur in advance so that they can make their code ready for the update, or ensure they 
    don't use the new version (see [version control](bumpversion.md)). You start to see why even making small 
    changes to well used codebases can result in all kinds of issues for developers down the line. 

!!! tip

     `pytest.approx` deals well with Numpy arrays!

## Using PyTest
[PyTest](https://docs.pytest.org) is an example of a _test runner_, which orchestrates the execution of tests and 
provides the outcome to the user. There are others available, including the in-built 
[`unittest`](https://docs.python.org/3/library/unittest.html) and [`nose`](https://nose.readthedocs.io/) to name a few.
However, PyTest is now one of the more widely used as it provides one of the most readable formats for unit tests, with
each test being an isolated function, rather than a method of a dedicated class.

### Organizing your test directory
So that PyTest knows where to look for unit tests, you need to ensure that the directory structure and filenames are
appropriate. To make your code readable it is advised you put them all in a directory called `tests` in the root of the 
repository. The structure of this directory is up to you, but it should make sense to the reader (e.g. one subdirectory 
per Python package). 

For each test file, it is essential that the name of file starts with `test` (as for the 
<a href="#method_names">method names</a>), so that PyTest knows to run it. This example project has the test files and 
folders structured as follows:

```{.bash}
pyosirix_example_project/ 
├── tests/                
│   └── utilities/                    # Matches package name being tested (1) 
│       ├── conftest.py
│       ├── test_text_2_image.py      # Module name with "test_" prefix (2)
│       └── test_unit_conversions.py  # Module name with "test_" prefix
```

1.  A Python _package_ is a directory of python files with a `__init__.py` file contained.
2.  A Python _module_ is a python file containing methods, classes and so on.

!!! note

    This project also contains a `pyosirix_operations` subpackage. Unfortunaately this does not lend itself well to
    unit testing as it requires OsiriX or Horos to be active when being used and is thus not automatable (at present).
    This is where the conecpt of _user testing_ becomes more appropriate, but we will not yet go into that here until
    the processes are more established within the pyOsiriX project itself.

### Sharing data using PyTest fixtures 
A pytest [__fixture__](https://docs.pytest.org/en/stable/reference/fixtures.html) is a piece of code that can be reused
across multiple test methods, in order to reduce code redundancy. This could, for example, be loading in test data or
defining a shared instance of some created Python class. There are four _scopes_ for each fixture:

1. `function`: set up and tear down the resource for each test function.
2. `class`: set up and tear down the resource for each test class.
3. `module`: set up and tear down the resource for each test file.
4. `session`: set up and tear down the resource for each test session (e.g. all test files being run).

If the fixture is defined within a test module, it is available only to those methods in the module. If it is defined in
a `conftest.py` file within the test package, then it is available to all modules within that package. The following 
examples demonstrate fixtures for testing the 
[numpy.sum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html) and 
[numpy.cumsum](https://numpy.org/doc/stable/reference/generated/numpy.cumsum.html) methods:

```{.py title="tests/conftest.py"}
----8<----
tests/conftest.py
----8<----
```

```{.py title="tests/numpy/test_numpy_sum.py"}
----8<----
tests/numpy/test_numpy_sum.py
----8<----
```

### Running PyTest.
Running PyTest for a single set of unit tests is as simple as running the following from your Terminal from the base 
directory of the repository:
```bash
python -m pytest tests/utilities/test_unit_conversions.py
```

The output should look something like:
```text
=============================== test session starts ================================
platform darwin -- Python 3.9.13, pytest-6.2.4, py-1.11.0, pluggy-0.13.1
rootdir: /Users/adminmblackledge/Documents/Projects/pyosirix_example_project
plugins: anyio-3.6.1, hydra-core-1.3.2, dvc-3.5.1
collected 2 items

tests/test_unit_conversions.py ..                                            [100%]

================================ 2 passed in 0.22s =================================
```
A nice concise indication that everything is working as expected.


Alternatively, if you want to run the entire unit test suite in the directory, you can run:
```bash
python -m pytest tests
```

If you use PyCharm to develop your code, it should also provide a little green play symbol 
(<span style="color:green">&#9654;</span>) next to the test function definition to run it in isolation (a great way to 
test your unit test!). You can also run the file to run all tests within the file - there are many options.

!!! note annotate

    As unit tests are so widely used the chances are that most IDEs (1) will have some functionality for running unit 
    tests graphically.

1.  IDE = Integrated Development Environment

## Automating unit tests with GitHub Actions
It is highly valuable to run unit tests on your code everytime you push changes to a repository like GitHub. This 
demonstrates to both yourself and any users that a particular code version has passed all checks and is still working
as anticipated. In GitHub this can be done using [actions](github.md), which are configured to run following certain
GitHub events (push, release and so on). In this project, unit tests are configured to run as defined in the 
`unittests.yaml` file (reproduced below). It will run every time code is pushed to the `main` or `dev` branches. You
would not need to change this if you follow the [steps above](#organizing-your-test-directory) for setting up your 
test directory structure.

```{.yaml title=".github/workflows/unittests.yaml"}
----8<----
.github/workflows/unittests.yaml
----8<----
```