<!-- Feel free to delete me in a forker repository -->
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

## Setting up your PyPI project
Setting up a PyPI project is pretty easy. You will need to have registered for an account on Python Package Index
[website](https://pypi.org/) (it's free!). It is also worth searching PyPI to check that your intended project name
has not already been taken (you will need to come up with an alternative if so).

It is also worth setting up an account on TestPyPI. This is a completely separate version of PyPI that acts as a 
staging ground for you to check all is in place before you commit to the main server. Once you have uploaded a 
package, it is bad practice to remove it and PyPI will complain if you try to upload the same version again. There
are other options, including "yanking" a specific release and some discussion of this can be found 
[here](https://snarky.ca/what-to-do-when-you-botch-a-release-on-pypi/). TestPyPI helps you determine everything is 
working _before_ the upload.

### The `pyproject.toml` file
Within your project repository you will need to define a configuration file that tells pip information about your 
project, including its name and version, the developers details, and a brief description. The `pyproject.toml` file 
is the current standard for doing this (superseding `setup.py`, which you may find in other projects). A _Tom's Obvious, 
Minimal Language_ (toml) file is designed to be easy to read by humans, providing all need configuration options in a 
single file (kind of!). There are several key sections to this file:

`[build-system]`

This tell pip which _backend_ to use. Here we use the default [setuptools](https://setuptools.pypa.io), but others 
exist, including [hatch](https://hatch.pypa.io). You can leave this as it is.
```{.toml title="[build-system] example"}
----8<----
pyproject.toml:2:4
----8<----
```

`[project]`

This defines project specific characteristics, which must be adapted to your project.
- `name`: The name of the project as it will be defined on PyPI (`pip install xyz`, where `name = "xyz"`).
- `version`: The package version. Should match that of your repository - see [bumpversion](bumpversion.md).
- `description`: A short description of your package.
- `authors`: A list, `[]`, of tables, `{}` defined in toml format describing the package authors.
- `maintainers`: Similar to above, but who is looking after the project moving forward.
- `readme`: Defines the information people will see when looking at your project on PyPI.
- `license`: The license file for your project. Let users know what they can do with your code - there are templates.
- `keywords`: List some keywords for PyPI. Perhaps this helps with a search, but I'm not entirely sure.
- `classifiers`: A list "Trove classifiers" for each release, describing who it's for, what systems it can run on, and 
   how mature it is (see [here](https://pypi.org/classifiers/) for a list).
```{.toml title="[project] example"}
----8<----
pyproject.toml:6:29
----8<----
```

`[tool.tool_name]`

This section is used for tool-specific configurations (setuptools in this instance). There are many options available 
depending on which back end you use so make sure to check out the documentation for a full breakdown. The ones below
are almost a bare minimum.
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

Below are the possible options for defining library versions:
```{.txt title="Example library definitions"}
requests>=2.25.1,<2.26.0
numpy==1.19.3
scipy<=1.6.0
pandas>=1.1.0
flask!=1.1.1
Django>=3.0,<4.0
colorama; sys_platform == "win32"
```

It is possible to automatically generate a requirements file using the `pip freeze > requirements.txt` command, but
this dumps _every_ library in your current environment, and it's specific version to file. This is far too restrictive 
for another user that might disagree with your choice of library version for something completely unrelated!

Another option is (__pipreqs__)[https://github.com/bndr/pipreqs], which searches through your project and creates a 
`requirements.txt` file based on your `import` statements. It is easy to install using
```bash
pip install pipreqs
```
My suggested use would then be
```bash
pipreqs . --force --mode gt
```
which would force an overwrite of your current requirements.txt file, ensuring that each library version is at least 
as new as that you have on your system. __Note__: Once you have created your `requirements.txt` file, it is worthwhile 
giving it a check and adding anything pipreqs has missed.

```{.txt title="requirements.txt for this project"}
----8<----
requirements.txt
----8<----
```

## Distributing your project
Once you are ready to distribute your project, this is done using two tools: `build` and `twine`.  These can be
installed using pip:
```bash
pip install build twine
```
Move to the root directory of your repository, and build a distribution.
```bash
python -m build
```

Now you can check everything is working as expected by uploading to TestPyPI:
```bash
python3 -m twine upload --repository testpypi dist/*
```
It will ask you for your PyPI login details, and once these are entered, your package should be available. It would be
good practice to check all is working well by creating a 
[new conda environment](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#creating-environments)
and trying to install your package by using (in the case of this project):
```bash
pip install -i https://test.pypi.org/simple/ pyosirix_example_project
```

Once you are happy with this then you can upload to the main server:
```bash
python3 -m twine upload --repository pypi dist/*
```
Again, it will ask you for your credentials, and then everything should be uploaded!

## Integration into GitHub Actions
Use of manual steps such as those above can lead to errors and does not fit in well with the concept of automated
"continuous integration/continuous development" (CI/CD). It can be much more effective to let GitHub take care of the 
upload to PyPI for you through [Actions](github.md). One of the issues with this is that it does not allow you to check 
how your library works on TestPyPI before the final upload. There are many solutions to this depending on your CI/CD 
workflow. 

In this project we do it by having two branches: "main" and "dev". GitHub Actions is configured to send to 
TestPyPI when code is pushed to the "dev" branch, and to PyPI when pushed to the "main" branch. GitHub will need to know
your login credentials to this for you, however.  Use the following steps for both PyPI and TestPyPI:

1. Login to your [PyPI account settings](https://test.pypi.org/manage/account/) or 
   [TestPyPI account settings](https://test.pypi.org/manage/account/).
2. Look for the section _API tokens_ and click "_Add API token_". 
3. Add a name for your token and select the scope to be just that of your project (see note below).
4. On the next page select the button "_Copy token_".
5. Go to your project on GitHub, and find your project "_Settings_" tab.
6. On the list of option on the left, find "_Secrets and variables_", and click on "_Actions_".
7. Click on "_New repository secret_".
8. Give your secret a name (`PYPI_TOKEN` for example), and paste the token in "_Secret_" box.
9. Click "_Add secret_".

__Note__: If you have not yet uploaded your project to PyPI or TestPyPI, you will not be able to reduce the token scope 
to just that project. One option is to perform a manual upload very early on in project development and call it 0.0.0
or something. Make sure to tell the user in the README that this version may not work!

```{.yaml title="GH Actions specification for PyPI upoload"}
----8<----
.github/workflows/pypi-distribution.yaml
----8<----
```
