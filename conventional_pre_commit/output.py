import os

from conventional_pre_commit.format import ConventionalCommit


class Colors:
    LBLUE = "\033[00;34m"
    LRED = "\033[01;31m"
    RESTORE = "\033[0m"
    YELLOW = "\033[00;33m"

    def __init__(self, enabled=True):
        self.enabled = enabled

    @property
    def blue(self):
        return self.LBLUE if self.enabled else ""

    @property
    def red(self):
        return self.LRED if self.enabled else ""

    @property
    def restore(self):
        return self.RESTORE if self.enabled else ""

    @property
    def yellow(self):
        return self.YELLOW if self.enabled else ""


def fail(commit: ConventionalCommit, use_color=True):
    c = Colors(use_color)
    lines = [
        f"{c.red}[Mensaje de commit incorrecto] >>{c.restore} {commit.message}"
        f"{c.yellow}Your commit message does not follow Conventional Commits formatting{c.restore}",
        f"{c.blue}https://dev.azure.com/ACTSIS/DEVOPS/_wiki/wikis/DEVOPS.wiki/106/Buenas-pr%C3%A1cticas-Git/{c.restore}",
    ]
    return os.linesep.join(lines)


def verbose_arg(use_color=True):
    c = Colors(use_color)
    lines = [
        "",
        f"{c.yellow}Usa el argumento {c.restore}--verbose{c.yellow} para más información.{c.restore}",
    ]
    return os.linesep.join(lines)


def fail_verbose(commit: ConventionalCommit, use_color=True):
    c = Colors(use_color)
    lines = [
        "",
        f"{c.yellow}Los mensajes de commit convencionales siguen un patrón como:",
        "",
        f"{c.restore}    type(scope): asunto",
        "",
        "    cuerpo extendido",
        "",
    ]

    def _options(opts):
        formatted_opts = f"{c.yellow}, {c.blue}".join(opts)
        return f"{c.blue}{formatted_opts}"

    errors = commit.errors()
    if errors:
        lines.append(f"{c.yellow}Por favor corrige los siguientes errores:{c.restore}")
        lines.append("")
        for group in errors:
            if group == "type":
                type_opts = _options(commit.types)
                lines.append(f"{c.yellow}  - Valor esperado para {c.restore}tipo{c.yellow} de: {type_opts}")
            elif group == "scope":
                if commit.scopes:
                    scopt_opts = _options(commit.scopes)
                    lines.append(f"{c.yellow}  - Valor esperado para {c.restore}scope{c.yellow} de: {scopt_opts}")
                else:
                    lines.append(
                        f"{c.yellow}  - Valor esperado para {c.restore}scope{c.yellow} pero no se encontró ninguno.{c.restore}"
                    )
            else:
                lines.append(
                    f"{c.yellow}  - Valor esperado para {c.restore}{group}{c.yellow} pero no se encontró ninguno.{c.restore}"
                )

    lines.extend(
        [
            "",
            f"{c.yellow}Run:{c.restore}",
            "",
            "    git commit --edit --file=.git/COMMIT_EDITMSG",
            "",
            f"{c.yellow}para editar el mensaje de commit y reintentar el commit.{c.restore}",
        ]
    )
    return os.linesep.join(lines)


def unicode_decode_error(use_color=True):
    c = Colors(use_color)
    return f"""
{c.red}[Mensaje de commit incorrecto encoding]{c.restore}

{c.yellow}conventional-pre-commit no pudo decodificar tu mensaje de commit.
Se asume codificación UTF-8, por favor configura git para escribir mensajes de commit en UTF-8.
See {c.blue}https://github.com/ACTSIS/conventional-pre-commit/#_discussion{c.yellow} para más información.{c.restore}
"""
