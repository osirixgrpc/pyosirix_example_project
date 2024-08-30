# Continuous Integration and Continuous Deployment (CI/CD) with GitHub
Continuous Integration and Continuous Deployment (CI/CD) are essential practices in modern software development, 
particularly in methodologies like DevOps and its AI-focused counterpart, MLOps. The primary goal of CI/CD is to 
encourage smaller, more frequent code updates, which comes with several benefits:

 - __Improved Code Quality__: Frequent updates allow for continuous testing and validation, catching bugs and issues 
   early in the development cycle.  CI/CD emphasizes a disciplined approach to coding, testing, and deploying that
   requires proper infrastructure and practices to be effective.
 - __Modular Updates__: By keeping changes small and focused, updates are easier to manage, test, and debug, enhancing 
   overall software design and maintainability. 
 - __Reduced Risk__: Smaller changes reduce the risk of large-scale failures, making the impact of any individual update 
   less severe. 
 - __Automated Quality Control__: Code quality checks using automated [unit testing](pytest.md) and linting ensure that
   all code is functional and follows proper stylistic conventions at regular intervals and before software release. 
 - __Faster Delivery__: Automated building and deployment streamline the process of delivering software 
   updates, keeping customers satisfied with quicker access to new features and fixes.

If you want to know more about the theory and practise of CI/CD there is a great 
[article by Red Hat](https://www.redhat.com/en/topics/devops/what-is-ci-cd) to get your started on your . 

CI/CD automation is managed in GitHub through [_Actions_](#actions), with bug reporting, project planning/maintenance, 
and software support provided through [_Issues_](#issues). Actions and issue templates are defined using YAML files, 
human-readable data structures often used for configuration of projects and data transfer. It is quite quick to learn
and more details can be found in this 
[nice tutorial](https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started).

## Actions
GitHub Actions provides support for automating processes within GitHub repositories. It is a highly flexible interface
that can allow you to automatically perform operations when some _trigger_ occurs within the repository. This could,
for example, be someone pushing code to the repository, creating a release of a specific version of your code, or even
somebody creating a new [issue](#issues). We can only cover the very basics here, but please see the 
[official documentation](https://docs.github.com/en/actions) provided by GitHub for a more in-depth discussion.


Actions are defined using YAML files contained within the following directory of your project:

```{.txt title="Location of files defining GitHub actions"}
.github/workflows/
```

The structure of these files is relatively straightforward once you get used to them. In this project, for example,
there is a `unittests.yaml` workflow that performs all [unit tests](pytest.md) everytime code is pushed to the 
`main` or `dev` branches. The content of this file is shown below - we will break down and explain each of the 
components later on.

```{.yaml title="Actions file for automated unit testing (.github/workflows/unittests.yaml)"}
----8<----
.github/workflows/unittests.yaml
----8<----
```

__The breakdown__

A YAML file is effectively a set of (potentially nested) `key: value` pairs, much like a dictionary in Python. The three 
top-level key-value pairs that _must_ be included in your workflow file are:

 - `name`: A string that will represent the name of your action. This is how you will identify the action within the 
   GitHub interface so call it something sensible.
 - `on`: When should the action run? In this instance, we have told it that this happens during a code `push` event to 
   either of the `main` or `dev` branches. You can list multiple events to trigger the same action. There is a complete
   list of [events that trigger workflow actions](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows)
   on the GitHub website.
 - `jobs`: A list of jobs to perform as part of this workflow. In this case there is only a single job, `run-tests`, 
   but there can be more than one. By default, jobs runs in parallel, but you can make them dependent on one another 
   (sequential) using the [`jobs.<job_id>.needs`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idneeds) 
   option.

!!! note

    In YAML, lists are defined by prefixing each element with a hyphen (`-`), without requiring a specific key for each 
    element. In the example above, each job in the GitHub Actions workflow is represented as a dictionary, where the key 
    is the `job-id`, and the value is a nested dictionary containing the job's details. 
   
    However, the steps within each job are defined as a list of dictionaries, without explicit keys. This approach 
    emphasizes that steps are executed sequentially, in the order they are listed, while jobs themselves can run in 
    parallel or in any order unless dependencies are explicitly defined.

!!! note

    Just like Python, YAML relies heavily on indentation to define the structure and hierarchy of the data. The level 
    of indentation indicates which elements are nested within others. In the examples below, the difference in the 
    indentation of the offices dictionary significantly alters the data structure:

     - In Definition A, the offices are associated with Alice specifically, as they are indented under her entry in the 
       people list.
     - In Definition B, the offices are not related to Bob at all. Instead, they are a separate top-level entry outside 
       the people list.

    ```{.yaml title="Definition A"}
    people:
        - name: "Alice"
          offices:
              - Address: 123 Old Bormpton Road, London, UK
              - Address: 15 Cotswold Road, Sutton, UK
    ```

    ```{.yaml title="Definition B"}
    people:
        - name: "Bob"
    offices:
        - Address: 123 Old Bormpton Road, London, UK
        - Address: 15 Cotswold Road, Sutton, UK
    ```

There are many options for jobs and their executed steps depending on what you need. We cannot list them all
here, but a complete list is provided in the [GitHub workflow syntax page](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobs).
We will go through one used in the example above

 - `jobs.<job-id>`: The first thing you will notice is that each job is given an ID at the top level. This can be 
   anything you like, but must only be constructed with alphanumeric, `_`, or `-` symbols (cannot start with  latter). 
   This is used to reference the job within the workflow file and is also visible on the GitHub actions interface.
   See [here](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_id) for 
   more information.
 - `jobs.<job-id>.runs-on`: Tell GitHub which _runner_ to use for the job. This is a virtual machine that can be used
   to run the job. If you are using a public repository, most are free, and if you have a private repository, you will 
   have some allotted free minutes, after which you will be charged (you can set up a spend limit cap, which it £0 by 
   default). Runners can be Linux, Windows or Mac based, and if you want to pay more, you can get machines with better 
   specifications (see [here](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources)
   for more information).
 - `jobs.<job-id>.steps`: Each job consists of a number of steps, which will run sequentially. In this example the steps 
   are
     1. Checkout the latest repository code (from the branch that initiated the action by default).
     2. Install Python on the virtual machine runner.
     3. Install any package dependencies for the unit tests (defined in the project `requirements.txt` files).
     4. Run the unit tests. 
 - `jobs.<job-id>.steps.name`: A name for the step. This is how you will identify it within the GitHub interface.
 - `jobs.<job-id>.steps.uses`: Some actions can be re-used! This is how you reference one of the GitHub boilerplate
   workflows (`actions/checkout@v4` to checkout your repository and `actions/setup-python@v5` to install Python), 
   a third party's workflow, or even one of your own.
 - `jobs.<job-id>.steps.with`: Defines the input parameters to the boilerplate action defined above. In this case, we
   tell `actions/checkout@v4` that we want Python version 3.
 - `jobs.<job-id>.steps.run`: This is where the magic happens! This is where you run commands, just as you would do on
   a Terminal on your own machine. If it's a single line command, then just a single line will suffice (as for the `Unit 
   tests` step in the example above). However, if you want to run multiple commands in a single step, the `|` symbol is
   used to indicate that a multi-line command prompt will follow (as for the `Install dependencies` step in the example 
   above).


## Issues
No matter how many unit tests you design, there will _always_ be a bug in your code that you did not anticipate. One of 
the most effective ways to test your code and catch these bugs is to ask your users to let you know if they encounter 
something during use (this is an essential part of _post-market surveillance_ when developing software as a medical 
device). However, for feedback to be structured and useful, it is important to make sure that your users have somewhere
to raise any _issues_ they encounter.

GitHub achieves this through [Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues),
where bugs, new feature requests and software updates can be reported, planned, fixed and released. Advantages to GitHub
issues include:

 - __Structured Feedback__: Using [issue templates](#issue-templates) you can configure how you get feedback from users
   in certain scenarios, such as bugs, feature requests, and documentation fixes. There are no rules for this and these
   templates are completely flexible.
 - __Transparency and Traceability__: GitHub Issues provide a transparent view of all ongoing work within a project. 
    This traceability helps maintain accountability and provides a historical record of how challenges were addressed,
    which is valuable for audits and reviews.
 - __Collaboration and Communication__: As issues in public repositories are openly available, users are able to see 
   whether their issues have been encountered by others, and read any feedback, instructions or fixes that were advised 
   by the community. This is a great way to get others to help with support and documentation. 
 - __Seamless Integration__: GitHub Issues is directly integrated with your code repository, allowing you to link issues 
   to code commits, pull requests, and branches. This makes it easy to track the status of code changes related to 
   specific issues.
 - __Customizable with Actions__: Workflows in GitHub Issues can be automated using [Actions](#actions) using triggers, 
   such as automatically closing issues when a pull request is merged or sending notifications when an issue is updated.
 - __Labels, Milestones, and Assignees__: Labels help categorize issues (e.g., bug, enhancement, question), milestones 
   group issues into specific phases or releases, and assignees clearly define ownership of tasks, helping teams stay 
   organized.

We will not go into the details of how you use Issues to report bugs and ask for feature requests in other projects, as
this ultimately depends on the project. However, we will go through the basics of making an _issue template_ so that you
can get feedback from users in a format that is helpful to you and your project in certain scenarios.

### Issue templates
Similar to [GitHub Actions](#actions), issue templates are YAML files stored with a particular directory within your 
project:

```{.txt title="Location of files defining GitHub issue templates"}
./github/ISSUE_TEMPLATE
```

Within this project, we have defined four issue templates. These will suffice as a default if you don't want to make 
your own changes, and will still be present in your fork.

 - `bug.yaml` is the template for bug reports.
 - `documentation.yaml` is the template for reporting documentation errors.
 - `feature_request.yaml` is how users ask for new features in the software.
 - `generic.yaml` is for anything not covered in the above three.

When editing one of the template files, it is important to be aware of what each of the yaml _keys_ for these files do:

 - `name`: A unique name for the issue so that users know to select the right one (required).
 - `description`: A description for the issue that appears in the user interface when choosing a template (required).
 - `title` : A default title that will be pre-populated in the issue submission form (optional).
 - `labels`: A list of all 
    [GitHub labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels) to be 
    automatically assigned to the issue (e.g "bug") (optional).
 - `assignees`: A list of assignees to be automatically assigned to handle this issue (optional).
 - `description`: Projects that any issues created with this template will automatically be added to. The format of 
    this key is `PROJECT-OWNER/PROJECT-NUMBER` (optional).
 - `body`: Where you define the fields of the issue form (required). 

Each field of the issue form is then defined following the `[body]` key using the following key-value pairs:

 - `[type]`: The type of field (required). Possible values include:

    - `checkboxes`: The user will select a number of checkboxes.
    - `dropdown`: The user will select one from a number of options.
    - `input`: The user will write a line of text.
    - `textarea`: The user can write multiple lines of text.
    - `markdown`: Provide extra information to the user (not editable).

 - `id`: A unique identifier (one word) for the element. Only use alphanumeric characters, `-`, and `_` (optional).
 - `attributes`: A set of key-value pairs that define the properties of the element (required).
 - `validations`: A set of key-value pairs that set constraints on the element (e.g. is it a required field) 
   (optional).

Values for the `attributes` key will be dependent on the type of field. For a full list of these please see the 
[official documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema).

The bug reporting template for this project is reproduced as an example below:

```{.yaml title="Issue template for a bug report (.github/ISSUE_TEMPLATE/bug.yaml)"}
----8<----
.github/ISSUE_TEMPLATE/bug.yaml
----8<----
```


