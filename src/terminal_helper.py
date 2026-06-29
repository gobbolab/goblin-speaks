import typer


def print_header(title: str):
    typer.secho("=" * 40, fg=typer.colors.BLUE, bold=True)
    typer.secho(f"     {title}", fg=typer.colors.BLUE, bold=True)
    typer.secho("=" * 40, fg=typer.colors.BLUE, bold=True)
