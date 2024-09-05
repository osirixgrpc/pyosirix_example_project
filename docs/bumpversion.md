# Version Control with `bump2version`

## Semantic versioning
It is essential that you signal to your users which version of your code they are using. This helps them to keep track 
of which version is compatible with whatever they plan to do in their own solutions, and helps you to communicate how 
drastic the changes are that you are making from one version to the next. It also helps you keep up to date with the 
changes you are making.

This is now done almost universally through [_semantic versioning_](https://semver.org/). It is a very clear and concise
standard, that is easy to interpret and include within your own software. In the below, we will unashamedly "borrow" the
definitions by the [semver organization](https://semver.org/) as it provides the clearest explanation of the core 
concepts.

```{.txt title="Structure of semantic versioning"}
MAJOR.MINOR.PATCH
```

Increment:

 - `MAJOR` version when you make incompatible API changes
 - `MINOR` version when you add functionality in a backward compatible manner
 - `PATCH` version when you make backward compatible bug fixes

There are a few rules that must be adhered to when updating your version:

 - All elements of the version number must be integers, without leading zeros.
 - During an update, elements can only _increase_ numerically. For instance: `1.9.0 -> 1.10.0 -> 1.11.0`.
 - Once a versioned package has been released, the contents of that version __must not__ be modified. Any modifications 
   __must__ be released as a new version.
 - `PATCH`:
    - __Must__ be incremented if only backward compatible bug fixes are introduced (an internal change that fixes 
    incorrect behavior). 
 - `MINOR`:
    - __Must__ be incremented if new, backward compatible functionality is introduced to the public API.
    - __Must__ be incremented if any public API functionality is marked as deprecated. 
    - __May__ include patch level changes. 
    - __Must__ be reset `PATCH` to 0 when minor version is incremented. 
 - `MAJOR`: 
    - __Must__ be incremented if any backward incompatible changes are introduced to the public API. 
    - __May__ include `MINOR` and `PATCH` level changes. 
    - __Must__ reset `PATCH` and `MINOR` versions to 0 when major version is incremented.
 - `MAJOR = 0` indicates initial development and anything __may__ change at any time. The public API should not
   be considered stable.
 - A _pre-release_ version __may__ be denoted by appending a hyphen (`-`) and a series of dot separated identifiers 
   immediately following the patch version (e.g. `1.1.3-dev.0` is a pre-release for stable version `1.1.3`). A 
   pre-release version indicates that the version is unstable. Pre-release identifiers __must__ follow these rules:
    - __Must__ comprise only ASCII alphanumerics and hyphens (`0-9A-Za-z-`). 
    - __Must not__ be empty. 
    - __Must_not__ include leading zeroes.

```{.txt title="Example of semantic version ordering"}
0.0.1-dev.0  (first development phase for version 0.0.1)
0.0.1-dev.1  (second development phase for version 0.0.1)
0.0.1-rc.0   (first release candidate for version 0.0.1)
0.0.1        (unstable release of version 0.0.1)
0.0.2-dev.0  (first development phase for version 0.0.2)
0.0.2-rc.0   (first release candidate for version 0.0.2)
0.0.2        (unstable release of version 0.0.2)
1.0.0        (stable release of version 1.0.0)
1.1.0        (stable release of version 1.1.0)
1.1.1        (stable release of version 1.1.1)
``` 

!!! note

    The rules for pre-release are designed to be quite flexible. This is perhaps where you will do most of your
    development work so it is worth making sure that whatever sytax you use, it makes some sense upfront. Also, it will
    be helpful to your users to indicate somewhere in your documentation what your coventions are for the pre-release
    phase to indicate where you are in the development cycle.  For example, in the OsiriXgrpc project this is:
    
     - `0.0.1-dev.0`: Unstable release in the development phase of the `dev` branch, first code push.
     - `0.0.1-dev.1`: Unstable release in the development phase of the `dev` branch, second code push.
     - `0.0.1-rc.0`: Unstable release in the release-candidate phase of the `dev` branch, first code push.
     - `0.0.1`: Unstable release in the `main` branch.
     - `1.0.0`: Stable release in the `main` branch.

    This tells users that if we are in a release-candidate phase, we will not accept any new feature requets until the 
    next development cycle begins.

## Semantic versioning with `bump2version`
As your project expands, there will likely be many files that contain a reference to the software version. In this 
project, for example, there is a `VERSION` file to make it very easy to find, but the version is also contained in the
`mkdocs.yaml` file so that all released documentation clearly shows the software version. In fact, there are
nine files that contain a reference to the version throughout the project.

We would not want to manually update these files every time we push or release code to GitHub. Worse yet, this would 
likely lead to errors. This is where [`bump2version`](https://pypi.org/project/bump2version/) application comes in. 
By including a simple `.bumpverision.cfg` configuration file at the root of your code repository, you can tell 
`bump2version` which files contain a version string _and_ define the version update rules. It can then 'bump' the 
version of your entire project with single command.

## Installing `bump2version`
Installing `bump2version` of your system is easy:

```bash
pip install bump2version
```

## The `.bumpversion.cfg` file
Let's take a look at the `.bumpversion.cfg` file contained within this project.

```{.cfg title=".bumpversion.cfg"}
----8<----
.bumpversion.cfg
----8<----
```

!!! info

    `{current_version}` and `{new_version}` are placeholders that will be filled in with the previous and new 
    version strings.

### `[bumpversion]`
This section defines the main settings for the version bumping process.

 - `current_version = 0.0.1-dev.13`: Specifies the current version of the project representing 
   `MAJOR.MINOR.PATCH-RELEASE.BUILD`. 
 - `commit = True`: Indicates that `bump2version` will automatically commit to the local git repository after a
    successful run.
 - `message = Bump version: {current_version} → {new_version}`: The message used after a successful git commit.
 - `tag = False`: Tell `bump2version` not to [tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging) the repository 
    after a successful bump. 
 - `parse = (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(\-(?P<release>[a-z]+).(?P<build>\d+))?`: This line defines a 
    [regular expression](https://docs.python.org/3/howto/regex.html) that bumpversion uses to parse the current version 
    string into different parts: major, minor, patch, release, and build. It is where you define the rules of your 
    versioning system. It is highly flexible, though of course here we have aligned with the 
    [semver conventions](#semantic-versioning). This way is pretty standard, and you can leave it as it is if you like.
 - `serialize`: Defines how the version string should be formatted when it is updated. In this case it can either be
   `MAJOR.MINOR.PATCH` or `MAJOR.MINOR.PATCH-RELEASE.BUILD` and nothing in between (for example `1.0.0-rc` would not
    be possible, and would not make sense as it must have a build number too).

!!! note

    The `\d+` statement oin the `parse` regular expression indicates that that component of the version string must be a 
    positive integer, which bumpversion handles by default for you. The `[a-z]+` indicates that this component must
    consist of a sequence of lowercase letters. `bump2version` does not handle this for you and you need to define the
    behaviour in the `[bumpversion:part:release]` of the configuration file.

### `[bumpversion:part:release]`
This section controls how the release part of the version is managed.

 - `first_value = dev`: Sets the default value of the release part to dev when first incremented.
 - `optional_value = void`: Specifies an optional value (void) that represents a missing or absent release type.
 - `values` Defines the allowed values for the release part of the version __in order__:
    - `dev`: Development release - still in the early stage of development (`dev` branch).
    - `rc`: Release candidate release - internally testing a potentially stable release. No new features (`dev` branch). 
    - `beta`: Beta release - external testing a potentially stable release (`main` branch).
    - `void`: No release type - this tells `bump2version` to move to a stable release (remove `-RELEASE.BUILD`).

### `[bumpversion:file:<file_path>]`
These sections specify the files where the version number should be updated. `bump2version` will search for the current 
version, defined by the `{current_version}` placeholder, and replace it with the new version, defined by the 
`{new_version}` placeholder.

 - `search`: Look for instances that match this string in the file.
 - `replace`: Replace the string with this one.

## Running `bump2version`

Running bumpversion is as simple as follows:

```bash
bumpversion <part>
```

where `<part>` indicates which part of the version you are trying to update. For example, say our starting version is
`1.1.1-dev.1`, below is a history of what happens depending on the bumpversion command you use:

| Command               | New version    |
|-----------------------|----------------|
| `bumpversion build`   | `1.1.1-dev.2`  |
| `bumpversion build`   | `1.1.1-dev.3`  |
| `bumpversion release` | `1.1.1-rc.0`   |
| `bumpversion build`   | `1.1.1-rc.1`   |
| `bumpversion release` | `1.1.1-beta.0` |
| `bumpversion release` | `1.1.1`        |
| `bumpversion minor`   | `1.2.0-dev.0`  |
| `bumpversion major`   | `2.0.0-dev.0`  |
| `bumpversion patch`   | `2.0.1-dev.0`  |

The name of `<part>` is completely dependent on the name you define for each part in the [`parse`](#bumpversion) field 
of the config file. 

!!! warning

    You must commit all your code changes _before_ running `bump2ersion` - it will fail and complain otherwise.  