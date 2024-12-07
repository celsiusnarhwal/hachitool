import os
import typing as t
from os import PathLike
from pathlib import Path

@t.overload
def set_output(name: str, value: str): ...

@t.overload
def set_output(data: dict): ...

@t.overload
def set_output(**kwargs): ...

@t.overload
def set_env(name: str, value: str): ...

@t.overload
def set_env(data: dict): ...

@t.overload
def set_env(**kwargs): ...

def add_path(path: str | os.PathLike): ...

def summary(content: str): ...