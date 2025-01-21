# conventional-pre-commit

Un hook de [`pre-commit`](https://pre-commit.com) para verificar que los mensajes de commit sigan el formato de
[Conventional Commits](https://conventionalcommits.org).

Funciona con Python >= 3.8.

## Uso

Asegúrate de que `pre-commit` esté [instalado](https://pre-commit.com#install).

Crea un archivo de configuración en blanco en la raíz de tu repositorio, si es necesario:

```console
touch .pre-commit-config.yaml
```

Agrega/actualiza `default_install_hook_types` y agrega una nueva entrada de repositorio en tu archivo de configuración:

```yaml
default_install_hook_types:
  - pre-commit
  - commit-msg

repos:
  # - repo: ...

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: <git sha o tag>
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: []
```

Instala el script de `pre-commit`:

```console
pre-commit install --install-hooks
```

Haz un commit (normal) :x::

```console
$ git commit -m "add a new feature"

[INFO] Initializing environment for ....
Conventional Commit......................................................Failed
- hook id: conventional-pre-commit
- duration: 0.07s
- exit code: 1

[Mensaje de commit incorrecto] >> add a new feature
Tu mensaje de commit no sigue el formato de Conventional Commits
https://dev.azure.com/ACTSIS/DEVOPS/_wiki/wikis/DEVOPS.wiki/106/Buenas-pr%C3%A1cticas-Git/
```

Y con el argumento `--verbose`:

```console
$ git commit -m "add a new feature"

[INFO] Initializing environment for ....
Conventional Commit......................................................Failed
- hook id: conventional-pre-commit
- duration: 0.07s
- exit code: 1

[Mensaje de commit incorrecto] >> add a new feature
Tu mensaje de commit no sigue el formato de Conventional Commits
https://dev.azure.com/ACTSIS/DEVOPS/_wiki/wikis/DEVOPS.wiki/106/Buenas-pr%C3%A1cticas-Git/

Los mensajes de commit convencionales siguen un patrón como:

    type(scope): asunto

    cuerpo extendido

Por favor corrige los siguientes errores:

  - Valor esperado para type de: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test

Ejecuta:

    git commit --edit --file=.git/COMMIT_EDITMSG

para editar el mensaje de commit y reintentar el commit.
```

Haz un commit (convencional) :heavy_check_mark::

```console
$ git commit -m "feat:92564 add a new feature"

[INFO] Initializing environment for ....
Conventional Commit......................................................Passed
- hook id: conventional-pre-commit
- duration: 0.05s
```

## Instalar con pip

`conventional-pre-commit` también se puede instalar y usar desde la línea de comandos:

```shell
pip install conventional-pre-commit
```

Luego ejecuta el script de línea de comandos:

```shell
conventional-pre-commit [types] input
```

- `[types]` es una lista opcional de tipos de Conventional Commit permitidos (por ejemplo, `feat fix chore`)

- `input` es un archivo que contiene el mensaje de commit a verificar:

```shell
conventional-pre-commit feat fix chore ci test .git/COMMIT_MSG
```

O desde un programa en Python:

```python
from conventional_pre_commit.format import is_conventional

# imprime True
print(is_conventional("feat:92564 this is a conventional commit"))

# imprime False
print(is_conventional("nope: this is not a conventional commit"))

# imprime True
print(is_conventional("custom: this is a conventional commit", types=["custom"]))
```

## Pasando `args`

`conventional-pre-commit` soporta varios argumentos para configurar su comportamiento:

```shell
$ conventional-pre-commit -h
usage: conventional-pre-commit [-h] [--no-color] [--force-scope] [--scopes SCOPES] [--strict] [--verbose] [types ...] input

Verifica si un mensaje de commit de git sigue el formato de Conventional Commits.

argumentos posicionales:
  types            Lista opcional de tipos a soportar.
  input            Un archivo que contiene un mensaje de commit de git.

opciones:
  -h, --help       muestra este mensaje de ayuda y sale
  --no-color       Desactiva los colores en la salida.
  --force-scope    Obliga a que el commit tenga un scope definido.
  --scopes SCOPES  Lista de scopes soportados. Los scopes deben estar separados por comas sin espacios (por ejemplo: api,cliente).
  --strict         Obliga a que el commit siga estrictamente el formato de Conventional Commits. No permite commits con fixup! ni merge.
  --verbose        Imprime mensajes de error más detallados.
```

Proporciona argumentos en la línea de comandos, o a través de la propiedad `hooks.args` de pre-commit:

```yaml
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: <git sha o tag>
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: [--strict, --force-scope, feat, fix, chore, test, custom]
```

**NOTE:** cuando se usa como un hook de pre-commit, `input` se proporciona automáticamente (con el mensaje del commit actual).

## Desarrollo

`conventional-pre-commit` viene con una configuración de [VS Code devcontainer](https://code.visualstudio.com/learn/develop-cloud/containers)
para proporcionar un entorno de desarrollo consistente.

Con la extensión `Remote - Containers` habilitada, abre la carpeta que contiene este repositorio dentro de Visual Studio Code.Code.

Deberías recibir un aviso en la ventana de Visual Studio Code; haz clic en  `Reopen in Container` para ejecutar el entorno de desarrollo dentro del devcontainer.

Si no recibes un aviso, o cuando sientas que necesitas comenzar desde un entorno nuevo:

1. `Ctrl/Cmd+Shift+P` para abrir el paleta de comandos en Visual Studio Code
1. Escribe `Remote-Containers` para filtrar los comandos
1. Selecciona `Rebuild and Reopen in Container` para reconstruir completamente el devcontainer
1. Selecciona `Reopen in Container` para reabrir la última construcción del devcontainer

## Versionado

El versionado generalmente sigue [Semantic Versioning](https://semver.org/).

## Haciendo un release

Los releases a PyPI y GitHub se activan al empujar una etiqueta.

1. Asegúrate de que todos los cambios para el release estén presentes en la rama `main`
1. Etiqueta con la nueva versión: `git tag vX.Y.Z` para un release, `git tag vX.Y.Z-preN` para un pre-release
1. Empuja la nueva etiqueta de versión: `git push origin vX.Y.Z`

## License

[Apache 2.0](LICENSE)

Inspired by matthorgan's [`pre-commit-conventional-commits`](https://github.com/matthorgan/pre-commit-conventional-commits).
