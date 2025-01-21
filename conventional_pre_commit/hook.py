import argparse
import sys

from conventional_pre_commit import output
from conventional_pre_commit.format import ConventionalCommit

RESULT_SUCCESS = 0
RESULT_FAIL = 1


def main(argv=[]):
    parser = argparse.ArgumentParser(
        prog="conventional-pre-commit",
        description="Verifica si un mensaje de commit de git sigue el formato de Conventional Commits.",
    )
    parser.add_argument(
        "types", type=str, nargs="*", default=ConventionalCommit.DEFAULT_TYPES, help="Lista opcional de tipos a soportar."
    )
    parser.add_argument("input", type=str, help="Un archivo que contiene un mensaje de commit de git.")
    parser.add_argument(
        "--no-color", action="store_false", default=True, dest="color", help="Desactiva los colores en la salida."
    )
    parser.add_argument(
        "--force-scope",
        action="store_false",
        default=True,
        dest="optional_scope",
        help="Fuerza a que el commit tenga un scope definido.",
    )
    parser.add_argument(
        "--scopes",
        type=str,
        default=None,
        help="Lista de scopes soportados. Los scopes deben estar separados por comas sin espacios (por ejemplo: api,cliente).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fuerza a que el commit siga estrictamente el formato de Conventional Commits. No permite commits con fixup! ni merge.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        dest="verbose",
        default=False,
        help="Imprime mensajes de error más detallados.",
    )

    if len(argv) < 1:
        argv = sys.argv[1:]

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return RESULT_FAIL

    try:
        with open(args.input, encoding="utf-8") as f:
            commit_msg = f.read()
    except UnicodeDecodeError:
        print(output.unicode_decode_error(args.color))
        return RESULT_FAIL
    if args.scopes:
        scopes = args.scopes.split(",")
    else:
        scopes = args.scopes

    commit = ConventionalCommit(commit_msg, args.types, args.optional_scope, scopes)

    if not args.strict:
        if commit.has_autosquash_prefix():
            return RESULT_SUCCESS
        if commit.is_merge():
            return RESULT_SUCCESS

    if commit.is_valid():
        return RESULT_SUCCESS

    print(output.fail(commit, use_color=args.color))

    if not args.verbose:
        print(output.verbose_arg(use_color=args.color))
    else:
        print(output.fail_verbose(commit, use_color=args.color))

    return RESULT_FAIL


if __name__ == "__main__":
    raise SystemExit(main())
