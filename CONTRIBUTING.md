# Contributing to Micro80

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to Micro80. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents
- [Contributing to Micro80](#contributing-to-micro80)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct ](#code-of-conduct-)
  - [How Can I Contribute? ](#how-can-i-contribute-)
    - [1. Reporting Bugs](#1-reporting-bugs)
    - [2. Suggesting Enhancements](#2-suggesting-enhancements)
    - [3. Contributing to the Code](#3-contributing-to-the-code)
  - [Style Guide ](#style-guide-)
  - [File Guide ](#file-guide-)

## Code of Conduct <a name = "code-of-conduct"></a>

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## How Can I Contribute? <a name = "how-can-i-contribute"></a>

### 1. Reporting Bugs

When Reporting Bugs, please check the following first.

- [ ] Check if the bug is already reported.
- [ ] Check if the code is the latest version.
- [ ] Check if the bug is not a feature.
  
If the bug is not reported, please open an issue with the following details.

- A clear and descriptive title.
- A description of what the bug is.
- Steps to reproduce the bug.
- What you expected to happen.
- What actually happened.
- Any other information that might be useful.

### 2. Suggesting Enhancements

When Suggesting Enhancements, please check the following first.

- [ ] Check if the enhancement is already suggested.
- [ ] Check if the enhancement doesn't go against the project's goals.

If the enhancement is not suggested, please open an issue with the following details.

- A clear and descriptive title.
- A description of what the enhancement is.
- How the enhancement would be useful.
- Any other information that might be useful.
- If you are willing to work on the enhancement, please mention it.

### 3. Contributing to the Code

When Contributing to the Code, please check the following first.

- [ ] Check if the feature/contribution is not already implemented.
- [ ] Check if the feature/contribution doesn't go against the project's goals.
- [ ] Check if the feature/contribution is not already in a PR by someone else.
  
> When editing, working with the code set-it up using the setup guide in the README.md file.

If the feature/contribution is not implemented, please open a pull request with the following details.

- A clear and descriptive title.
- A description of what the feature/contribution is.
- How the feature/contribution would be useful.
- Any other information that might be useful.

## Style Guide <a name = "style-guide"></a>

The Code Style/Format is maintained using the Black Code Formatter. Please make sure to run the code through the formatter before making a pull request.

```bash
python -m black .
```

The code should also be well documented and should follow the PEP8 guidelines.

## File Guide <a name = "file-guide"></a>

The code is written in Cython's Pure Python Mode.

so, `*.py` are the normal python code. and `*.pxd` are the Cython Declarations. (In a sense these are the header files)

`.c` files are the cython generated C files, you need them when running but do not include them in the PR

And That's it! 🎉

Happy Contributing! 🚀
