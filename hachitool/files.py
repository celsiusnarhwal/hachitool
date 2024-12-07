import os
from enum import StrEnum
from pathlib import Path
import typing as t

from multimethod import multimethod
from pydantic import validate_call, ConfigDict

__all__ = ["set_output", "set_env", "add_path", "summary"]


class File(StrEnum):
    OUTPUT = "OUTPUT"
    ENV = "ENV"
    PATH = "PATH"
    SUMMARY = "STEP_SUMMARY"

    def write(self, content: str):
        fp = Path(os.getenv("GITHUB_" + self.value))
        fp.open("a", newline="\n").write(content)


@multimethod
def _write_kv(file: File, key: t.Any, value: t.Any):
    file.write(f"{key}={value}")


@multimethod
def _write_kv(file: File, data: dict):
    for key, value in data.items():
        _write_kv(file, key, value)


@multimethod
def _write_kv(file: File, **kwargs):
    _write_kv(file, kwargs)


def set_output(*args, **kwargs):
    _write_kv(File.OUTPUT, *args, **kwargs)


def set_env(*args, **kwargs):
    _write_kv(File.ENV, *args, **kwargs)


@validate_call
def add_path(path: Path):
    File.PATH.write(str(path))


@validate_call(config=ConfigDict(coerce_numbers_to_str=True))
def summary(content: str):
    File.SUMMARY.write(content)
