<!-- Feel free to delete me in a forked repository -->
# Python Package Index (PyPI)
Once you've developed your code in a version-controlled repository, sharing the project with other users gives you kudos
and (hopefully) makes the software world a better and more efficient place. However, users might not want to download 
the entire project repository, which could include unnecessary files like unit tests, configuration files, and other 
superfluous data. A more efficient way to share your code is by using the Python Package Index (PyPI). PyPI allows you 
to distribute version-controlled packages easily and manages installation and dependencies through `pip`, ensuring a 
smooth experience for both you and your users. Installing your code becomes as simple as `pip install my_project`.

Here are some basic instructions to help you get started. For more detailed guidance, refer to the [official pip 
documentation](https://pip.pypa.io/en/stable/reference/build-system/) and the default backend for pip, 
[setuptools](https://setuptools.pypa.io/en/stable/userguide/).

## Setting up a PyPI account

To upload projects to PyPI, you first need to create a free account on the [PyPI website](https://pypi.org/). 
Additionally, it's highly recommended to set up an account on [TestPyPI](https://test.pypi.org/), a separate version of 
PyPI designed as a staging environment. This allows you to verify that everything works correctly before committing to 
the main PyPI server.

Once a package is uploaded to PyPI, it’s considered bad practice to remove it, and PyPI will prevent you from 
re-uploading the same version. If you encounter issues with a release, there are alternatives, such as "yanking" a 
specific release. You can read more about these options 
[here](https://snarky.ca/what-to-do-when-you-botch-a-release-on-pypi/). Using TestPyPI helps ensure that everything is 
functioning correctly before you make your final upload to PyPI.

### PyPI tokens
PyPI no longer supports upload of projects using standard login credentials, and instead requires you to use 
[_PyPI tokens_](https://pypi.org/help/#apitoken) to verify account access. These tokens are either limited to a specific 
project or can provide access to all projects in your account. Once created, PyPI will only show you this token once,
so you will need to copy it somewhere safe. To create a token, follow these steps:

1. Login to your [PyPI account settings](https://test.pypi.org/manage/account/) or 
   [TestPyPI account settings](https://test.pypi.org/manage/account/).
2. Look for the section _API tokens_ and click "_Add API token_". 
3. Add a name for your token and select the scope to be either project specific or for the entire account.
4. On the next page select the button "_Copy token_".

It is much safer to create a project-specific token. However, if the project does not yet exist on PyPI you will need 
to upload the project for the first time using an account-wide token. Perhaps the best way to do this is by storing 
one within a [`.pypirc` configuration file](https://packaging.python.org/en/latest/specifications/pypirc/) on your
machine:

1. In Terminal, use `touch ~/.pypirc`
2. Open the file (`open ~/.pypirc`) and configure it to look as shown:
```{.toml title=".pypirc contents example"}
[pypi]
username = __token__
password = <PyPI token>

[testpypi]
username = __token__
password = <TestPyPI token>
```
where `<PyPI token>` and `<TestPyPI token>` are the tokens generated for you by PyPI and TestPyPI respectively.
3. The file stores your token in plain text. Ensure you are the only person who can read the file by typing 
   `chmod 600 ~/.pypirc`.


If you feel at any point that these tokens may have been compromised (e.g. computer loss), you can easily delete these
tokens on the PyPI/TestPyPI websites and create new ones.

## Setting up a PyPI project
Distributing your project to PyPI is quite straightforward, but requires some set-up at the beginning of your project 
through two key configuration files, `pyproject.toml` and `requirements.txt`. 

### The `pyproject.toml` file
Within your project repository you will need to define a configuration file that tells pip information about your 
project, such as its name and version, the developers details, and a brief description. The `pyproject.toml` file 
is the current standard for doing this (superseding `setup.py`, which you may find in other projects). A _Tom's Obvious, 
Minimal Language_ (toml) file is designed to be easy to read by humans, providing all required configuration options in 
a single file. The key sections to this file are:

#### `[build-system]`

This tells pip which _backend_ to use. Here we use the default [setuptools](https://setuptools.pypa.io), but others 
exist, including [hatch](https://hatch.pypa.io). You can leave this as it is.
```{.toml title="[build-system] example"}
----8<----
pyproject.toml:2:4
----8<----
```

#### `[project]`

This defines project specific characteristics, which must be adapted for your project.
- `name`: The name of the project as it will be defined on PyPI (`pip install xyz`, where `name = "xyz"`).
- `version`: The package version. Should match that of your repository - see [bumpversion](bumpversion.md).
- `description`: A short description of your package.
- `authors`: A list, `[]`, of tables, `{}` defined in toml format describing the package authors.
- `maintainers`: Similar to above, but who is looking after the project moving forward.
- `readme`: Defines the information people will see when looking at your project on PyPI.
- `license`: The license file for your project. Let users know what they can do with your code - there are 
   [templates](https://opensource.org/licenses) to choose from.
- `keywords`: List some keywords for PyPI. Perhaps this helps with a search, but I'm not entirely sure.
- `classifiers`: A list "Trove classifiers" for each release, describing who it's for, what systems it can run on, and 
   how mature it is (see [here](https://pypi.org/classifiers/) for a list).
```{.toml title="[project] example"}
----8<----
pyproject.toml:6:29
----8<----
```

#### `[tool.tool_name]`

This section is used for tool-specific configurations (setuptools in this instance). There are many options available 
depending on which back end you use so make sure to check out the documentation for a full breakdown. The ones below
are a bare minimum.
- `packages`: Tells pip the name of the packages that will be installed (in python use `import xyz` if 
  `packages = ["xyz"]`). Must reflect the name of the directory where the source code is located!
- `dependencies`: Tells pip what the essential libraries are for compatability (see 
   [requirements](#the-requirementstxt-file)).
```{.toml title="[tool.tool_name] example"}
----8<----
pyproject.toml:31:
----8<----
```

### The `requirements.txt` file

This file lists all the dependencies of this project. Here we use the bare minimum and just define the names of 
important packages.  However, it is also standard to define which version of the library you need. I have found that
the more stringent the library version, and the more libraries needed, the higher the chance you might run into conflict
on some else's machine.

Below are the possible options for defining ranges of library versions:
```{.python title="Example library definitions"}
requests>=2.25.1,<2.26.0    # Must be within a range of versions
numpy==1.19.3               # Must be a specific version
scipy<=1.6.0                # Must be at least as old as a particular version
pandas>=1.1.0               # Must be at least as new as a particular version
flask!=1.1.1                # Must not be a specific version
```

It is possible to automatically generate a requirements file using the `pip freeze > requirements.txt` command, but
this dumps _every_ library in your current environment, and it's specific version to file. This is far too restrictive 
for another user who might disagree with your choice of library version for something completely unrelated.

A better option is (__pipreqs__)[https://github.com/bndr/pipreqs], which searches through your project and creates a 
`requirements.txt` file based on your `import` statements. It is easy to install using
```bash
pip install pipreqs
```
A suggested use would then be
```bash
pipreqs . --force --mode gt
```
which would force an overwrite of your current requirements.txt file, ensuring that each library version is at least 
as new as the one on your system. __Note__ that once you have created your `requirements.txt` file, it is worthwhile 
giving it a check and adding anything pipreqs may have missed!

```{.txt title="requirements.txt for this project"}
----8<----
requirements.txt
----8<----
```

## Project distribution (manual approach)
Once you are ready to distribute your project, this is done using two tools: `build` and `twine`: 

1. Ensure that both libraries are up-to-date
```bash
pip install --upgrade build twine
```

2. Ensure that dependent libraries within `requirements.txt` are installed:
```bash
pip install -r requirements.txt
```

3. Move to the root directory of your repository, and build a distribution.
```bash
cd /path/of/repo
python -m build
```
When successful, this should create a `dist` directory within your project (ensure that this is included in your
`.gitignotre` file).

4. Upload to TestPyPI:
```bash
twine upload --repository testpypi dist/*
```
5. Check all is working well by creating a 
[new conda environment](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#creating-environments)
and trying to install your package by using (in the case of this project):
```bash
pip install -i https://test.pypi.org/simple/ pyosirix_example_project
```

6. Once you are happy with this then you can upload to the main server:
```bash
twine upload --repository pypi dist/*
```

## Distribution with GitHub (automatic approach)
Use of manual steps such as those above can lead to errors and does not fit in well with the concept of automated
"continuous integration/continuous development" (CI/CD). It can be much more effective to let GitHub take care of the 
upload to PyPI for you through [Actions](github.md). One of the issues with this is that it does not allow you to check 
how your library works on TestPyPI before the final upload to PyPI. There are multiple solutions to this, but in this 
project we do it by having two branches: "main" and "dev". GitHub Actions is configured to send to upload to TestPyPI 
when code is pushed to the "dev" branch, and to PyPI when pushed to the "main" branch.

GitHub allows you store sensitive information, such as PyPI/TestPyPI tokens as a project-specific _secret_, which may
then be used by Actions to automatically provide login credentials. These are not observable to collaborators on a 
project, but with certain access may be used by them when performing actions from their account. It is a good idea
to ensure, however, that these tokens are only project specific in scope. However, If you have not yet uploaded your 
project to PyPI or TestPyPI, you will not yet be able to generate a project-specific token. So it is advised that the
first upload be performed manually, using your account token.

To add a token to GitHub secrets, perform the following:

1. [Generate a token](#pypi-tokens) as above, ensuring its scope is only for the project.
2. Go to your project on GitHub, and find your project "_Settings_" tab.
3. On the list of options on the left, select "_Secrets and variables_" then click on "_Actions_".
4. Click on "_New repository secret_".
5. Give your secret a name, `PYPI_TOKEN` for example, but it must match the name used in the 
   [workflow yaml file](github.md) for the Action (see example below).
6. Paste the token in "_Secret_" box.
7. Click "_Add secret_".

```{.yaml title="GH Actions specification for PyPI upoload"}
----8<----
.github/workflows/pypi-distribution.yaml
----8<----
```