import re
from typing import List


class Commit:
    """
    Clase base para inspeccionar el formato de mensajes de commit.
    """

    AUTOSQUASH_PREFIXES = sorted(
        [
            "amend",
            "fixup",
            "squash",
        ]
    )

    def __init__(self, commit_msg: str = ""):
        self.message = str(commit_msg)
        self.message = self.clean()

    @property
    def r_autosquash_prefixes(self):
        """Cadena regex para prefijos de autosquash."""
        return self._r_or(self.AUTOSQUASH_PREFIXES)

    @property
    def r_verbose_commit_ignored(self):
        """Cadena regex para la parte ignorada de un mensaje de commit detallado."""
        return r"^# -{24} >8 -{24}\r?\n.*\Z"

    @property
    def r_comment(self):
        """Cadena regex para comentarios."""
        return r"^#.*\r?\n?"

    def _r_or(self, items):
        """Une elementos con el símbolo "|" para formar un OR en regex."""
        return "|".join(items)

    def _strip_comments(self, commit_msg: str = ""):
        """Elimina comentarios de un mensaje de commit."""
        commit_msg = commit_msg or self.message
        return re.sub(self.r_comment, "", commit_msg, flags=re.MULTILINE)

    def _strip_verbose_commit_ignored(self, commit_msg: str = ""):
        """Elimina la parte ignorada de un mensaje de commit detallado."""
        commit_msg = commit_msg or self.message
        return re.sub(self.r_verbose_commit_ignored, "", commit_msg, flags=re.DOTALL | re.MULTILINE)

    def clean(self, commit_msg: str = ""):
        """
        Elimina comentarios y segmentos ignorados de un mensaje de commit.
        """
        commit_msg = commit_msg or self.message
        commit_msg = self._strip_verbose_commit_ignored(commit_msg)
        commit_msg = self._strip_comments(commit_msg)
        return commit_msg

    def has_autosquash_prefix(self, commit_msg: str = ""):
        """
        Devuelve True si la entrada comienza con uno de los prefijos de autosquash utilizados en git.
        Consulta la documentación: https://git-scm.com/docs/git-rebase.
        """
        commit_msg = self.clean(commit_msg)
        pattern = f"^(({self.r_autosquash_prefixes})! ).*$"
        regex = re.compile(pattern, re.DOTALL)

        return bool(regex.match(commit_msg))

    def is_merge(self, commit_msg: str = ""):
        """
        Devuelve True si la entrada comienza con "Merge branch".
        Consulta la documentación: https://git-scm.com/docs/git-merge.
        """
        commit_msg = self.clean(commit_msg)
        return commit_msg.lower().startswith("merge branch ")


class ConventionalCommit(Commit):
    """
    Implementa verificaciones para el formato de Conventional Commits.

    https://www.conventionalcommits.org
    """

    CONVENTIONAL_TYPES = sorted(["feat", "fix"])
    DEFAULT_TYPES = sorted(
        CONVENTIONAL_TYPES
        + [
            "build",
            "chore",
            "ci",
            "docs",
            "perf",
            "refactor",
            "revert",
            "style",
            "test",
            "wip",
        ]
    )

    def __init__(
        self, commit_msg: str = "", types: List[str] = DEFAULT_TYPES, scope_optional: bool = True, scopes: List[str] = []
    ):
        super().__init__(commit_msg)

        if set(types) & set(self.CONVENTIONAL_TYPES) == set():
            self.types = self.CONVENTIONAL_TYPES + types
        else:
            self.types = types
        self.types = sorted(self.types) if self.types else self.DEFAULT_TYPES
        self.scope_optional = scope_optional
        self.scopes = sorted(scopes) if scopes else []

    @property
    def r_types(self):
        """Cadena regex para tipos válidos."""
        return self._r_or(self.types)

    @property
    def r_id(self):
        """Expresión regular para el identificador numérico requerido después del delimitador."""
        return r"\d{1,9}"

    @property
    def r_subject(self):
        """Cadena regex para la línea de asunto, asumiendo que tras el ID habrá un espacio y luego el mensaje."""
        # Aseguramos que haya un espacio luego del número y el resto del mensaje
        return r" .+$"

    @property
    def r_scope(self):
        """Cadena regex para un scope opcional o requerido con formato específico."""
        if self.scopes:
            scopes = self._r_or(self.scopes)
            escaped_delimiters = list(map(re.escape, [":", ",", "-", "/"]))
            delimiters_pattern = self._r_or(escaped_delimiters)
            scope_pattern = rf"\(\s*(?:{scopes})(?:\s*(?:{delimiters_pattern})\s*(?:{scopes}))*\s*\)"

            if self.scope_optional:
                return f"(?:{scope_pattern})?"
            else:
                return scope_pattern

        if self.scope_optional:
            return r"(\([\w \/:,-]+\))?"
        else:
            return r"(\([\w \/:,-]+\))"

    @property
    def r_delim(self):
        """Cadena regex para un indicador opcional de cambio importante y el delimitador de dos puntos."""
        return r"!?:"

    @property
    def r_body(self):
        """Cadena regex para el cuerpo, con soporte multilinea."""
        return r"(?P<multi>\r?\n(?P<sep>^$\r?\n)?.+)?"

    @property
    def regex(self):
        """`re.Pattern` para el formato de Conventional Commits."""
        types_pattern = f"^(?P<type>{self.r_types})?"
        scope_pattern = f"(?P<scope>{self.r_scope})?"
        # Combina el delimitador, el ID numérico y el asunto
        delim_pattern = f"(?P<delim>{self.r_delim})"
        id_pattern = f"(?P<id>{self.r_id})"
        subject_pattern = f"(?P<subject>{self.r_subject})?"
        body_pattern = f"(?P<body>{self.r_body})?"

        pattern = types_pattern + scope_pattern + delim_pattern + id_pattern + subject_pattern + body_pattern

        return re.compile(pattern, re.MULTILINE)

    def errors(self, commit_msg: str = "") -> List[str]:
        """
        Devuelve una lista de componentes faltantes de Conventional Commits en un mensaje de commit.
        """
        commit_msg = self.clean(commit_msg)

        missing = []

        # Verificar el 'type'
        if not re.match(rf"^{self.r_types}", commit_msg):
            missing.append("type")

        # Verificar el 'scope' si no es opcional
        if not self.scope_optional:
            if not re.match(rf"^{self.r_types}\({self.r_scope}\)", commit_msg):
                missing.append("scope")
        else:
            # Si el scope es opcional pero presente, verificar su validez
            scope_match = re.match(rf"^{self.r_types}\({self.r_scope}\)", commit_msg)
            if scope_match and not scope_match.group("scope"):
                missing.append("scope")

        # Verificar el 'delim'
        if not re.search(rf"{self.r_delim}", commit_msg):
            missing.append("delim")

        # Verificar el 'id'
        if not re.search(rf"{self.r_delim}\s*\d{{1,9}}", commit_msg):
            missing.append("id")

        # Verificar el 'subject'
        subject_match = re.search(rf"{self.r_subject}", commit_msg)
        if not subject_match:
            missing.append("subject")

        # Verificar 'body' y 'sep'
        # Determinar si hay un cuerpo presente (un salto de línea seguido de texto)
        body_present = bool(re.search(r"\r?\n.+", commit_msg))
        if body_present:
            # Verificar si hay una línea en blanco (sep) antes del cuerpo
            # Esto significa que hay dos saltos de línea consecutivos
            if not re.search(r"\r?\n\r?\n.+", commit_msg):
                missing.append("sep")

        return missing

    def is_valid(self, commit_msg: str = "") -> bool:
        """
        Devuelve True si el mensaje de commit cumple con el formato de Conventional Commits.
        https://www.conventionalcommits.org
        """

        match = self.match(commit_msg)

        # match all the required components
        #
        #    type(scope): asunto
        #
        #    cuerpo extendido
        #
        return bool(match) and all(
            [
                match.group("type"),
                self.scope_optional or match.group("scope"),
                match.group("delim"),
                match.group("subject"),
                any(
                    [
                        # no extra body; OR
                        not match.group("body"),
                        # a multiline body with proper separator
                        match.group("multi") and match.group("sep"),
                    ]
                ),
            ]
        )

    def match(self, commit_msg: str = ""):
        """
        Devuelve un objeto `re.Match` para la entrada que cumple con el formato de Conventional Commits.
        """
        commit_msg = self.clean(commit_msg) or self.message
        return self.regex.match(commit_msg)


def is_conventional(
    input: str, types: List[str] = ConventionalCommit.DEFAULT_TYPES, optional_scope: bool = True, scopes: List[str] = []
) -> bool:
    """
    Devuelve True si la entrada cumple con el formato de Conventional Commits.
    https://www.conventionalcommits.org

    Opcionalmente, se puede proporcionar una lista de tipos personalizados adicionales.
    """
    commit = ConventionalCommit(commit_msg=input, types=types, scope_optional=optional_scope, scopes=scopes)

    return commit.is_valid()
