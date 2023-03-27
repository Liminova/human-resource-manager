# The python-project Contributing Guide

## Setting up your Git repository

You should fork the repository by hitting the Fork button on GitHub. This will
create a copy of the repository on your account that you can do anything with.
Afterwards, you should clone the repository to your local machine, using:

- If you're using HTTPS:

```shell
$ git clone https://github.com/<USERNAME>/python-project
```

- If you're using SSH:

```shell
$ git clone git@github.com:<USERNAME>/python-project
```

Replace `<USERNAME>` with your GitHub username.

You should also set your Git configuration to automatically rebase on pulls.
This cleans up your own fork, and in turn, the main branch from merge commits
when you try to sync up code with the main branch.

```shell
$ git config --global pull.rebase true
```

## Development requirements

This repository uses Python 3.10 and `pipenv`. If you don't already have
`pipenv`, follow the instructions to setting the repository up for usage in the
[README](README.md) file.

This repository uses [commitlint](https://commitlint.js.org) to lint commits,
with the [Conventional Commits](https://www.conventionalcommits.org) format.
For the best experience in committing code, you should have
[Node.js](https://nodejs.org) installed on your local machine. Afterwards:

- Install [pnpm](https://pnpm.io). This repository mainly uses `pnpm` (as shown
  by the `pnpm-lock.yaml` file) but you can use anything. `pnpm` simply gives
  the sanest defaults and the best performance. If you use anything else (`npm`
  or `yarn`), please add their respective lockfiles - `package-lock.json` and
  `yarn.lock` into the `.gitignore` file.

```shell
$ npm i -g pnpm
```

- Install dependencies using `pnpm`:

```shell
$ pnpm i
```

- Every time you want to commit something, use `pnpm cz` after adding files
  with `git add`. This will give you an automated prompt to fill in the
  details of your commit, according to the Conventional Commits format.
