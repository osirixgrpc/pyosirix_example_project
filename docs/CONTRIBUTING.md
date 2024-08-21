# Contributing
Thanks for your interest in this project - we welcome your help and support!

## Ways to Contribute
<table>
  <tr>
    <td><b>Documentation</b></td>
    <td>We encourage feedback on our documentation to improve the user experience and ensure it makes sense. Please see 
        our <a href="#documentation">instructions for project documentation</a> for more information.</td>
  </tr>
  <tr>
    <td><b>Testing</b></td>
    <td>We greatly appreciate our testers, who provide core feedback and have a key role in deciding the future of the 
        project. Please <a href="#contact">contact us</a> if you would like to become an official tester!</td>
  </tr>
  <tr>
    <td><b>Bug Tracking</b></td>
    <td>We will endeavour to fix all bugs encountered as soon as possible. If you encounter a bug, please see our 
        <a href="#bug-reporting">bug reporting</a> section.</td>
  </tr>
  <tr>
    <td><b>Feature Suggestions</b></td>
    <td>We cannot improve things without good ideas coming from users. If you would like to request a new feature this 
        can be done as a feature request on the project    
        <a href="https://github.com/osirixgrpc/pyosirix_example_project/issues"> issue tracker</a>.  Please note that 
        acceptance and importance of features will be discussed and agreed by our developers following discussion with 
        you. We cannot guarantee that all feature requests will be implemented, or how quickly they will be 
        delivered.</td>
  </tr>
  <tr>
    <td><b>Feature Development</b></td>
    <td>If you would like to help develop this project, we are keen to improve and evolve every aspect of it. This 
      includes: 
      <ul>
        <li>Optimize CI/CD (all performed in GitHub)</li>
        <li>Improve the user experience</li>
        <li>Ensure that key updates to libraries are monitored and fixed within the project.</li>
      </ul>
      Please see the remainder of this documentation to see how this can be done, and <a href="contact">let us 
      know</a> about your ideas!</td>
  </tr>
</table>

## Code of Conduct
Please see our [Code of Conduct](CODE_OF_CONDUCT.md) for more information.

## Prerequisites
In order to help contribute to this project there are a few things you will need. Some may not be required 
depending on the level contributions you want to make.

<table>
  <tr>
    <td><b>Mac</b></td>
    <td>OsiriX works on macOS.  We currently support (and have tested) compatability of OsiriXgrpc on macOS Monterey and
        above, on both Intel and M1/M2/M3 native processors. We always advise ensuring that your operating system is 
        up-to-date.</td>
  </tr>
  <tr>
    <td><b>OsiriX or Horos</b></td>
    <td>A copy of the <a href="https://www.osirix-viewer.com/osirix/osirix-md/download-osirix-lite/">latest OsiriX 
        app</a> downloaded on your system. This will be crucial for testing the OsiriXgrpc plugin, developing new 
        features, and authoring new OsiriXgrpc scripts. A free alternative is 
        <a href="https://horosproject.org/">Horos</a>.</td>
  </tr>
  <tr>
    <td><b>GitHub Account</b></td>
    <td>You will need a GitHub account to interact with the source code, create pull requests for new
        features that you have developed, and raise new issues or report bugs on the project 
        <a href="https://github.com/osirixgrpc/pyosirix_example_project/issues"> issue tracker</a>.</td>
  </tr>
</table>

## Coding Guidelines
### Project Structure
There are several core files and directories at the [root of the project](https://github.com/osirixgrpc/pyosirix_example_project)

| Name                    | Description                                                                                                |
|-------------------------|------------------------------------------------------------------------------------------------------------|
| __.github__             | Issue templates and CI/CD workflows for GitHub Actions.                                                    |
| __data__                | The location for external data. This will not be tracked by Git and data will be downloaded during set-up. |
| __docs__                | All externally-facing documentation (definition files in markdown).                                        |
| __pyosirix_operations__ | Source code for integrating the project code into OsiriX/Horos through pyOsiriX.                           |
| __tests__               | Automatic unit tests for the project.                                                                      |
| __utilities__           | General utilities for use within the project.                                                              |
| .bumpversion.cfg        | Rules to increment version numbers scattered throughout the project.                                       |
| .gitignore              | What Git will __not__ keep track of during version control.                                                |
| LICENSE                 | The license for all code within this project.                                                              |
| mkdocs.yaml             | The configuration file for creating documentation with MkDocs.                                             |
| pyproject.toml          | The configuration file for packaging and uploading this project to the Python Package Index.               |
| README.md               | A symlink to the projects main README.md file located within the __docs__ directory.                       |
| requirements.txt        | The core library requirements for the project.                                                             |
| VERSION                 | A simple file containing the current version of the project as a string.                                   |

### Modifying Source Code
When making changes to the source code, we recommend the following process to ensure your contributions can be 
efficiently reviewed and integrated:

1. __Fork the Repository__ Start by forking the repository. This creates your own copy of the project where you can make 
   your changes. 
3. __Make Your Changes__ Implement your changes in your forked repository. To facilitate a smooth review process, we 
   suggest:
    - Isolate Changes: Keep your changes focused. Large or complex modifications may require more extensive review and 
      have a higher chance of being rejected.
    - Communicate Intentions: Let us know about your planned changes in advance. This helps us coordinate contributions 
      and include them in our release planning.
4. __Submit a Pull Request (PR)__ Once you're satisfied with your changes, submit them back to the main project via a 
   pull request. Ensure your PR targets an appropriate branch. For guidance on creating a pull request, see GitHub's 
   [documentation](https://docs.github.com/articles/creating-a-pull-request-from-a-fork) on Creating a pull request from 
   a fork. 
5. __Review Process__ Your pull request will undergo a review by the project maintainers. During this phase:
    - Merge Upstream Changes: You may be asked to merge changes from the upstream branch into your fork to resolve 
      any conflicts.
6. __Final Steps__ After addressing any review comments and completing the version bump, your changes will be merged into 
   the project.

__Additional Tips for a Successful Contribution__

  - __Follow Coding Standards__ Adhere to the coding standards and guidelines provided in the repository documentation to 
    increase the likelihood of your changes being accepted. 
  - __Test Thoroughly__ Before submitting your pull request, thoroughly test your changes to ensure they work as expected 
    and do not introduce any new issues.

By following these guidelines, you can contribute valuable improvements to osirixgrpc and help enhance its 
functionality and user experience.

### Version Control
This project uses semantic versioning (`major.minor.patch-releasebuild`). Any release with `major` = 0 means that we may 
make subtle changes to the technology prior to 1.0.0 (i.e. no promises!).

Versioning is controlled by [bump2version](https://pypi.org/project/bump2version/). Below are the
commands available to bump2version within this project, and example increments in each case:
<table>
  <tr>
    <td><code>bumpversion build</code></td>
    <td>1.0.0-dev0 &rarr; 1.0.0-dev1 &rarr; 1.0.0-dev2 &rarr; ... <br> <i>or</i> <br>
        1.0.0-rc0 &rarr; 1.0.0-rc1 &rarr; 1.0.0-rc2 &rarr; ...</td>
  </tr>
  <tr>
    <td><code>bumpversion release</code></td>
    <td>1.0.0-dev5 &rarr; 1.0.0-rc0 &rarr; 1.0.0-beta0 &rarr; 1.0.0</td>
  </tr>
  <tr>
    <td><code>bumpversion patch</code></td>
    <td>1.0.0 &rarr; 1.0.1-dev0 &rarr; 1.0.2-dev0 &rarr; ...</td>
  </tr>
  <tr>
    <td><code>bumpversion minor</code></td>
    <td>1.0.2 &rarr; 1.1.0-dev0 &rarr; 1.2.0-dev0 &rarr; ...</td>
  </tr>
  <tr>
    <td><code>bumpversion major</code></td>
    <td>1.2.0 &rarr; 2.0.0-dev0 &rarr; 3.0.0-dev0 &rarr; ...</td>
  </tr>
</table>

## Documentation
All documentation is written in Markdown format and compiled using [MkDocs](https://www.mkdocs.org/). The organization 
of documentation should be kept consistent, and any changes to layout need to be fully discussed and agreed with all
developers before being implemented. 

| Name               | Description                                                                       |
|--------------------|-----------------------------------------------------------------------------------|
| assets             | Location for all figures and other supporting information not in Markdown format. |
| CODE_OF_CONDUCT.md | Our Code of Conduct                                                               |
| CONTRIBUTING.md    | Instruction for how to contribute to the project.                                 |
| mkdocs.yaml        | yaml configuration file for the mkdocs build                                      | 
| README.md          | The homepage for the documentation.                                               |

### Requirements
Building documentation requires both [mkdocs](https://www.mkdocs.org/) and 
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/) to be installed.  These can be installed using the 
`requirements.txt` file within the `docs` folder:
```bash
pip install -r docs/requirements.txt
```

### Building Documentation
To build the documentation from source it is sufficient to run the following command, from the `docs` folder within the
project root:
```bash
mkdocs build
```
This will create a new directory, `site`, which contains all built html documentation for deployment.

When developing documentation, however, it can be beneficial to run the MkDocs server (again from the `docs` folder):
```bash
mkdocs serve
```
By connecting to the established service (linking to `http://localhost:8000/` in a web-browser), it is then possible to 
view changes to documentation in real-time.

### Deploying Documentation
Collaborators should not directly modify the deployed documentation. Instead, this will be performed as part of 
continuous integration. Documentation will be deployed from the `main`branch following a push to the GitHub repository:

| Branch | Site                                                                                                           |
|--------|----------------------------------------------------------------------------------------------------------------|
| `main` | [https://osirixgrpc.github.io/pyosirix_example_project](https://osirixgrpc.github.io/pyosirix_example_project) |

### Suggesting Changes
If you would like to suggest a change to the documentation please let us know through the project 
<a href="https://github.com/osirixgrpc/pyosirix_example_project/issues"> issue tracker</a>, ensuring you 
choose a `documentation` label for the issue. If you wish to help contribute to the documentation, then please fork the
latest copy of the repository, modify it, and submit a pull request to the main branch. 

## Bug Reporting
If you encounter any bugs with this project then please let us know through the 
<a href="https://github.com/osirixgrpc/pyosirix_example_project/issues"> issue tracker</a>, ensuring you choose a 
`bug` label.  When you raise the issue, please using the relevant template for bugs, which will include the following 
information:

<ul>
  <li> What happened? </li>
  <li> What did you expect to see? </li>
  <li> What was the error message (if applicable)? </li>
  <li> What steps could we use to reproduce the bug? </li>
  <li> Project version. </li>
  <li> macOS version. </li>
  <li> Processor (Intel or Mac M1/M2/M3). </li>
</ul>

# Feature Requests
We warmly invite fresh insights and suggestions for enhancing this project. Every piece of feedback is invaluable to us. 
While we are committed to incorporating your suggestions to the best of our ability, please remember that this project 
thrives on community involvement and operates on a voluntary basis. Consequently, we cannot provide specific timelines 
for the introduction of new features.

If you wish request new features, please use our 
<a href="https://github.com/osirixgrpc/pyosirix_example_project/issues"> issue tracker</a> ensuring that you use a 
`feature request` label, using the `feature_request` issue template.  This includes the following information
<ul>
  <li>Short description of the new functionality</li>
  <li>Why would this improve the functionality of the project?</li>
  <li>Have you been using any work-around so far?</li>
  <li>How urgent is the new functionality to you?</li>
  <li>Would you be willing to help develop/test the new functionality?</li>
</ul>

## Issues
Please use the relevant label for each issue that you submit on the GitHub project.

| Label             | Description                                                                                                                                           |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `bug`             | If you encounter a bug then please let us know using the provided template. See [Bug Reporting](#bug-reporting) for more information.                 |
| `feature_request` | What else would you like see in this project? We welcome suggestions.                                                                                 |
| `documentation`   | Tell us how we can improve our [documentation](#documentation). This includes everything from fixing spelling mistakes to improving interpretability. |
| `generic`         | Any other issue you have with this project.                                                                                                           |


## Contact
| Name                | Contact                      |
|---------------------|------------------------------|
| Matt Blackledge     | matthew.blackledge@icr.ac.uk |