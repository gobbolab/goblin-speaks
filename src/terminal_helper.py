import typer


def print_header(title: str):
    typer.secho("=" * 40, fg=typer.colors.BLUE, bold=True)
    typer.secho(f"     {title}", fg=typer.colors.BLUE, bold=True)
    typer.secho("=" * 40, fg=typer.colors.BLUE, bold=True)


def print_logo(version: str):
    typer.secho(r"""
     _____       _     _ _         _____                  _
    |  __ \     | |   | (_)       /  ___|                | |
    | |  \/ ___ | |__ | |_ _ __   \ `--. _ __   ___  __ _| | _____
    | | __ / _ \| '_ \| | | '_ \   `--. \ '_ \ / _ \/ _` | |/ / __|
    | |_\ \ (_) | |_) | | | | | | /\__/ / |_) |  __/ (_| |   <\__ \
     \____/\___/|_.__/|_|_|_| |_| \____/| .__/ \___|\__,_|_|\_\___/
                                        | |
                                        |_|
          """, fg=typer.colors.BLUE, bold=True)
    typer.secho(f"                Penny Arcade Framework - {version}", fg=typer.colors.BLUE, bold=True)
    typer.echo("")
