<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</p>
<p align="center">
    <h1 align="center">ROBOTXT Parser</h1>
</p>
<p align="center">
    <em><code>Python library for fetching, parsing, and evaluating robots.txt rules for web crawlers</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/BedeschiL/robot_txt?style=default&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/BedeschiL/robot_txt?style=default&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/BedeschiL/robot_txt?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/BedeschiL/robot_txt?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<hr>

##  Quick Links

> - [ Overview](#-overview)
> - [ Features](#-features)
> - [ Repository Structure](#-repository-structure)
> - [ Modules](#-modules)
> - [ Getting Started](#-getting-started)
>   - [ Installation](#-installation)
>   - [ Running robot_txt](#-running-robot_txt)
>   - [ Tests](#-tests)
> - [ Project Roadmap](#-project-roadmap)
> - [ Contributing](#-contributing)
> - [ License](#-license)
> - [ Acknowledgments](#-acknowledgments)

---

##  Overview

A lightweight Python package that retrieves a site's robots.txt file, parses directives (User-agent, Allow, Disallow, Crawl-delay, Sitemap), and evaluates crawl permissions according to Google guidelines.

---

##  Features

- Fetch and cache robots.txt content
- Extract crawl-delay settings per user-agent
- List sitemap URLs declared in robots.txt
- Determine allowed and disallowed paths for specified user-agents
- Utility to test path access rules

---

##  Repository Structure

```sh
└── robot_txt/
    ├── main.py
    └── requirements.txt
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                    | Summary                         |
| ---                                                                                     | ---                             |
| [requirements.txt](https://github.com/BedeschiL/ROBOTXT_parser/blob/master/requirements.txt) | Lists Python dependencies: requests, pytest |
| [main.py](https://github.com/BedeschiL/ROBOTXT_parser/blob/master/main.py)                   | Implements RobotParser class and CLI entry point |

</details>

<details closed><summary>.idea</summary>

| File                                                                              | Summary                         |
| ---                                                                               | ---                             |
| [.gitignore](https://github.com/BedeschiL/robot_txt/blob/master/.idea/.gitignore) | <code>► INSERT-TEXT-HERE</code> |

</details>

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `>=3.7`

###  Installation

1. Clone the robot_txt repository:

```sh
git clone https://github.com/BedeschiL/robot_txt
```

2. Change to the project directory:

```sh
cd robot_txt
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

###  Running robot_txt

Use the following command to run robot_txt:

```sh
python main.py
```

###  Tests

To execute tests, run:

```sh
pytest
```

---

##  Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github/BedeschiL/robot_txt/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github/BedeschiL/robot_txt/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github/BedeschiL/robot_txt/issues)**: Submit bugs found or log feature requests for Robot_txt.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/BedeschiL/robot_txt
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  License

This project is protected under the [MIT License](LICENSE). For more details, see the [LICENSE](LICENSE) file.

---

##  Acknowledgments

- Developed by BedeschiL with inspiration from Google robots.txt guidelines
- Uses the Requests library: https://docs.python-requests.org/
- Regex parsing adapted from standard robots.txt parsing examples

[**Return**](#-quick-links)

---
