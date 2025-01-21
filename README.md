# conventional-pre-commit

A [`pre-commit`](https://pre-commit.com) hook to check commit messages for
[Conventional Commits](https://conventionalcommits.org) formatting.

Works with Python >= 3.8.

## Usage

Make sure `pre-commit` is [installed](https://pre-commit.com#install).

Create a blank configuration file at the root of your repo, if needed:

```console
touch .pre-commit-config.yaml
```

Add/update `default_install_hook_types` and add a new repo entry in your configuration file:

```yaml
default_install_hook_types:
  - pre-commit
  - commit-msg

repos:
  # - repo: ...

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: <git sha or tag>
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: []
```

Install the `pre-commit` script:

```console
pre-commit install --install-hooks
```

Make a (normal) commit :x::

```console
$ git commit -m "add a new feature"

[INFO] Initializing environment for ....
Conventional Commit......................................................Failed
- hook id: conventional-pre-commit
- duration: 0.07s
- exit code: 1

[Mensaje de commit incorrecto] >> add a new feature
Your commit message does not follow Conventional Commits formatting
https://dev.azure.com/ACTSIS/DEVOPS/_wiki/wikis/DEVOPS.wiki/106/Buenas-pr%C3%A1cticas-Git/
```

And with the `--verbose` arg:

```console
$ git commit -m "add a new feature"

[INFO] Initializing environment for ....
Conventional Commit......................................................Failed
- hook id: conventional-pre-commit
- duration: 0.07s
- exit code: 1

[Mensaje de commit incorrecto] >> add a new feature
Your commit message does not follow Conventional Commits formatting
https://dev.azure.com/ACTSIS/DEVOPS/_wiki/wikis/DEVOPS.wiki/106/Buenas-pr%C3%A1cticas-Git/

Los mensajes de commit convencionales siguen un patrón como:

    type(scope): asunto

    cuerpo extendido

Por favor corrige los siguientes errores:

  - Valor esperado para type de: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test

Run:

    git commit --edit --file=.git/COMMIT_EDITMSG

para editar el mensaje de commit y reintentar el commit.
```

Make a (conventional) commit :heavy_check_mark::

```console
$ git commit -m "feat: add a new feature"

[INFO] Initializing environment for ....
Conventional Commit......................................................Passed
- hook id: conventional-pre-commit
- duration: 0.05s
```

## Install with pip

`conventional-pre-commit` can also be installed and used from the command line:

```shell
pip install conventional-pre-commit
```

Then run the command line script:

```shell
conventional-pre-commit [types] input
```

- `[types]` is an optional list of Conventional Commit types to allow (e.g. `feat fix chore`)

- `input` is a file containing the commit message to check:

```shell
conventional-pre-commit feat fix chore ci test .git/COMMIT_MSG
```

Or from a Python program:

```python
from conventional_pre_commit.format import is_conventional

# prints True
print(is_conventional("feat: this is a conventional commit"))

# prints False
print(is_conventional("nope: this is not a conventional commit"))

# prints True
print(is_conventional("custom: this is a conventional commit", types=["custom"]))
```

## Passing `args`

`conventional-pre-commit` supports a number of arguments to configure behavior:

```shell
$ conventional-pre-commit -h
usage: conventional-pre-commit [-h] [--no-color] [--force-scope] [--scopes SCOPES] [--strict] [--verbose] [types ...] input

Verifica si un mensaje de commit de git sigue el formato de Conventional Commits.

positional arguments:
  types            Lista opcional de tipos a soportar.
  input            Un archivo que contiene un mensaje de commit de git.

options:
  -h, --help       show this help message and exit
  --no-color       Desactiva los colores en la salida.
  --force-scope    Fuerza a que el commit tenga un scope definido.
  --scopes SCOPES  Lista de scopes soportados. Los scopes deben estar separados por comas sin espacios (por ejemplo: api,cliente).
  --strict         Fuerza a que el commit siga estrictamente el formato de Conventional Commits. No permite commits con fixup! ni merge.
  --verbose        Imprime mensajes de error más detallados.
```

Supply arguments on the command-line, or via the pre-commit `hooks.args` property:

```yaml
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: <git sha or tag>
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: [--strict, --force-scope, feat, fix, chore, test, custom]
```

**NOTE:** when using as a pre-commit hook, `input` is supplied automatically (with the current commit's message).

## Development

`conventional-pre-commit` comes with a [VS Code devcontainer](https://code.visualstudio.com/learn/develop-cloud/containers)
configuration to provide a consistent development environment.

With the `Remote - Containers` extension enabled, open the folder containing this repository inside Visual Studio Code.

You should receive a prompt in the Visual Studio Code window; click `Reopen in Container` to run the development environment
inside the devcontainer.

If you do not receive a prompt, or when you feel like starting from a fresh environment:

1. `Ctrl/Cmd+Shift+P` to bring up the command palette in Visual Studio Code
1. Type `Remote-Containers` to filter the commands
1. Select `Rebuild and Reopen in Container` to completely rebuild the devcontainer
1. Select `Reopen in Container` to reopen the most recent devcontainer build

## Versioning

Versioning generally follows [Semantic Versioning](https://semver.org/).

## Making a release

Releases to PyPI and GitHub are triggered by pushing a tag.

1. Ensure all changes for the release are present in the `main` branch
1. Tag with the new version: `git tag vX.Y.Z` for regular release, `git tag vX.Y.Z-preN` for pre-release
1. Push the new version tag: `git push origin vX.Y.Z`

## License

[Apache 2.0](LICENSE)

Inspired by matthorgan's [`pre-commit-conventional-commits`](https://github.com/matthorgan/pre-commit-conventional-commits).
