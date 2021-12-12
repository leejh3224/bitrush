from dotenv import load_dotenv
from os import path
import pathlib

load_dotenv(dotenv_path=path.join(pathlib.Path().resolve(), ".env"))

import typer

from cli.account import account_app


app = typer.Typer()

app.add_typer(account_app, name="account")

if __name__ == "__main__":
    app()
