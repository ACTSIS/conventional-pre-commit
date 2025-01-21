import os

import pytest

from conventional_pre_commit.format import ConventionalCommit
from conventional_pre_commit.output import Colors, fail, fail_verbose, unicode_decode_error


@pytest.fixture
def commit():
    return ConventionalCommit("commit msg")


def test_colors():
    colors = Colors()

    assert colors.blue == colors.LBLUE
    assert colors.red == colors.LRED
    assert colors.restore == colors.RESTORE
    assert colors.yellow == colors.YELLOW

    colors = Colors(enabled=False)

    assert colors.blue == ""
    assert colors.red == ""
    assert colors.restore == ""
    assert colors.yellow == ""


def test_fail(commit):
    output = fail(commit)

    assert Colors.LRED in output
    assert Colors.YELLOW in output
    assert Colors.LBLUE in output
    assert Colors.RESTORE in output

    assert "Mensaje de commit incorrecto" in output
    assert "commit msg" in output
    assert "formato de Conventional Commits." in output
    assert "https://dev.azure.com/ACTSIS/DEVOPS/_wiki/wikis/DEVOPS.wiki/106/Buenas-pr%C3%A1cticas-Git/" in output


def test_fail__no_color(commit):
    output = fail(commit, use_color=False)

    assert Colors.LRED not in output
    assert Colors.YELLOW not in output
    assert Colors.LBLUE not in output
    assert Colors.RESTORE not in output


def test_fail_verbose(commit):
    commit.scope_optional = False
    output = fail_verbose(commit)

    assert Colors.YELLOW in output
    assert Colors.RESTORE in output

    output = output.replace(Colors.YELLOW, Colors.RESTORE).replace(Colors.RESTORE, "")

    assert "Los mensajes de commit convencionales siguen un patrón como:" in output
    assert f"type(scope): asunto{os.linesep}{os.linesep}    cuerpo extendido" in output
    assert "Valor esperado para tipo de: " in output
    for t in commit.types:
        assert t in output
    assert "Valor esperado para scope pero no se encontró ninguno." in output
    assert "git commit --edit --file=.git/COMMIT_EDITMSG" in output
    assert "para editar el mensaje de commit y reintentar el commit." in output


def test_fail_verbose__no_color(commit):
    output = fail_verbose(commit, use_color=False)

    assert Colors.LRED not in output
    assert Colors.YELLOW not in output
    assert Colors.LBLUE not in output
    assert Colors.RESTORE not in output


def test_fail_verbose__optional_scope(commit):
    commit.scope_optional = True
    output = fail_verbose(commit, use_color=False)

    assert "Valor esperado para scope pero no se encontró ninguno." not in output


def test_fail_verbose__missing_subject():
    commit = ConventionalCommit("feat(scope):92564", scope_optional=False)
    output = fail_verbose(commit, use_color=False)

    assert "Valor esperado para subject pero no se encontró ninguno." in output
    assert "Valor esperado para type pero no se encontró ninguno." not in output
    assert "Valor esperado para scope pero no se encontró ninguno." not in output


def test_fail_verbose__no_body_sep():
    commit = ConventionalCommit(
        scope_optional=False,
        commit_msg="""feat(scope):92564 subject
body without blank line
""",
    )

    output = fail_verbose(commit, use_color=False)

    assert "Valor esperado para sep pero no se encontró ninguno." in output
    assert "Valor esperado para multi pero no se encontró ninguno." not in output

    assert "Valor esperado para subject pero no se encontró ninguno." not in output
    assert "Valor esperado para type pero no se encontró ninguno." not in output
    assert "Valor esperado para scope pero no se encontró ninguno." not in output


def test_fail_no_id():
    """
    Prueba que verifica que falta el 'id' en el mensaje de commit.
    """
    # Mensaje de commit con type y scope válidos, y subject, pero sin id
    commit_message = "feat(scope): subject"
    commit = ConventionalCommit(commit_msg=commit_message, scope_optional=False)
    output = fail_verbose(commit, use_color=False)

    # Verificar que el error de 'id' está presente en la salida
    expected_error = "  - Valor esperado para id (Número del requerimiento) pero no se encontró ninguno."
    assert expected_error in output, f"Se esperaba el error de 'id' en la salida, pero no se encontró. Salida: {output}"

    # Asegurarse de que no haya otros errores inesperados
    assert "Valor esperado para tipo pero no se encontró ninguno." not in output, "No se esperaba un error de 'type'."
    assert "Valor esperado para scope pero no se encontró ninguno." not in output, "No se esperaba un error de 'scope'."
    assert "Valor esperado para subject pero no se encontró ninguno." not in output, "No se esperaba un error de 'subject'."


def test_valid_commit():
    """
    Prueba que verifica que un mensaje de commit válido no reporte errores.
    """
    # Mensaje de commit válido con type, scope, id y subject
    commit_message = "feat(scope):123 Implementar nueva funcionalidad"
    commit = ConventionalCommit(commit_msg=commit_message, scope_optional=False)
    output = fail_verbose(commit, use_color=False)

    # No debería haber mensajes de error
    assert "Por favor corrige los siguientes errores:" not in output, "No se esperaban errores para un commit válido."


def test_unicode_decode_error():
    output = unicode_decode_error()

    assert Colors.LRED in output
    assert Colors.YELLOW in output
    assert Colors.LBLUE in output
    assert Colors.RESTORE in output

    assert "Mensaje de commit incorrecto encoding" in output
    assert "Se asume codificación UTF-8, por favor configura git para escribir mensajes de commit en UTF-8." in output
    assert "https://github.com/ACTSIS/conventional-pre-commit/#_discussion" in output


def test_unicode_decode_error__no_color():
    output = unicode_decode_error(use_color=False)

    assert Colors.LRED not in output
    assert Colors.YELLOW not in output
    assert Colors.LBLUE not in output
    assert Colors.RESTORE not in output
