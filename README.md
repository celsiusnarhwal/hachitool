# Hachitool

Hachitool is a set of utilities that make it easier to work with Python scripts in GitHub Actions.

## Installation

Hachitool can be installed like any other Python package:

```yaml
- run: pip install hachitool
```

### Inline scripts

Hachitool can be ephemerally installed for inline Python scripts via [uv](https://docs.astral.sh/uv):

```yaml
- uses: astral-sh/setup-uv@v3

- shell: uv run --with hachitool python {0}
  run: |
    import hachitool

    # Do stuff here
```

### External scripts

Hachitool can be emphemerally installed for external scripts via uv and
[inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata):

```python
# script.py

# /// script
# dependencies = [
#     "hachitool",
# ]
# ///

import hachitool

# Do stuff here
```

```yaml
# workflow.yml

- uses: astral-sh/setup-uv@v3

- run: uv run script.py
```

## Usage

### `hachitool.set_output`

[Set output parameters for a step](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#setting-an-output-parameter).
Takes either:

- a key as its first argument and a value as its second
- a set of key-value pairs as either a dictionary or keyword arguments

```python
import hachitool

# All of these are equivalent
hachitool.set_output("key", "value")
hachitool.set_output({"key": "value"})
hachitool.set_output(key="value")
```

### `hachitool.set_env`

[Set environment variables](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#setting-an-environment-variable).
Takes either:

- a key as its first argument and a value as its second
- a set of key-value pairs as either a dictionary or keyword arguments

```python
import hachitool

# All of these are equivalent
hachitool.set_env("key", "value")
hachitool.set_env({"key": "value"})
hachitool.set_env(key="value")
```

### `hachitool.add_path`

Append something to the system path.

```python
import hachitool

hachitool.add_path("/absolute/or/relative/path")
```

### `hachitool.summary.add`

Add content to
the [step summary](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#adding-a-job-summary).
Supports [GitHub-flavored Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

```python
import hachitool

hachitool.summary.add("this is a summary")
```

> [!TIP]
> Calling `hachitool.summary` directly does the same thing:
> ```python
> import hachitool
>    
> hachitool.summary("this is a summary")
> ```

If the keyword-only `overwrite` argument is `True`, existing summary content will be erased:

```python
import hachitool

hachitool.summary.add("this is a summary", overwrite=True)
```

### `hachitool.summary.clear`

Clear the step summary.

```python
import hachitool

hachitool.summary.clear()
```

### `hachitool.mask`

[Mask a value](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#masking-a-value-in-a-log).

```python
import hachitool

hachitool.mask("super secret value")
```

### `hachitool.log`

Print a message to the log. Takes the following arguments:

| **Argument** | **Type**                                            | **Description**                                                                                                             | **Required?** |
|--------------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|---------------|
| `level`      | `"debug"` \| `"notice"` \| `"warning"` \| `"error"` | The log level of the message.                                                                                               | Yes           |
| `message`    | `str`                                               | The message to print.                                                                                                       | Yes           |
| `file`       | `str`                                               | The path to a file to annotate with the message.                                                                            | No            |
| `line`       | `int` \| `tuple[int, int]`                          | The line(s) of `file` to annotate with the message. A tuple will be interpreted as a pair of starting and ending lines.     | No            |
| `column`     | `int` \| `tuple[int, int]`                          | The column(s) of `file` to annotate with the message. A tuple will be interpreted as a pair of starting and ending columns. | No            |                                                                                                   |          

`level` and `message` are the first and second positional arguments, respectively.
`file`, `line`, and `column` are keyword-only.

```python
import hachitool

hachitool.log("notice", "this is a notice message", file="main.py", line=1, column=6)

# Using tuples for `line` and `column`
hachitool.log("notice", "this is a notic message", file="main.py", line=(1, 5), column=(6, 10))
```

### `hachitool.debug`, `hachitool.notice`, `hachitool.warning`, `hachitool.error`

Print a `debug`, `notice`, `warning`, or `error` message to the log, respectively. Takes all arguments of
`hachitool.log` except for `level`.

```python
import hachitool

hachitool.debug("this is a debug message")
hachitool.notice("this is a notice message")
hachitool.warning("this is a warning message")
hachitool.error("this is an error message")
```

### `hachitool.fail`

Optionally print an error-level message, then fail the workflow. Takes an optional `exit_code` argument
that must be an integer greater than or equal to 1. Additionally takes all arguments of `hachitool.error`,
except `message` is optional.

```python
import hachitool

hachitool.fail("something went wrong", exit_code=1)
```

### `hachitool.log_group`

Anything printed to the log inside this context manager will be nested inside an
[expandable group](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#grouping-log-lines).

Takes a mandatory `title` argument.

```python
import hachitool

with hachitool.log_group(title="group title"):
    print("I'm part of a log group!")
    print("me too!")
    print("me three!")
```

### `hachitool.literal`

Nothing printed to the log inside this context manager will be interpreted as a workflow command.

```python
import hachitool

hachitool.warning("this is a warning message to show that commands are being processed")

with hachitool.literal():
    hachitool.warning("this will not render as a warning because commands are not being processed")

hachitool.warning("this will render as a warning since commands are being processed again")
```