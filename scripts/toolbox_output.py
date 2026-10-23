#!/usr/bin/env python
"""Python 2.7 and Python 3 terminal output for standalone installers."""
from __future__ import print_function

from datetime import datetime
import os
import re
import sys


class TerminalOutput(object):
    """Render human-facing installer messages and prompts."""

    def __init__(self, tool_name, stream=None, clock=None, color=None):
        """Initialize a formatter.

        Args:
            tool_name (str): Catalog tool name.
            stream (file): Output stream. Defaults to standard output.
            clock (callable): Optional deterministic clock.
            color (bool): Optional explicit color support.
        """
        self.tool_name = tool_name
        self.stream = stream or sys.stdout
        self.clock = clock or (lambda: datetime.now().strftime("%H:%M:%S"))
        self.color = self._detect_color() if color is None else color
        self.started = False

    def _detect_color(self):
        return (
            "NO_COLOR" not in os.environ
            and os.environ.get("TERM") != "dumb"
            and hasattr(self.stream, "isatty")
            and self.stream.isatty()
        )

    def line(self, level, message, color_code=""):
        """Write a prefixed message at one semantic level."""
        if not self.started:
            self.stream.write("\n")
            self.started = True
        parts = str(message).splitlines() or [""]
        for part in parts:
            rendered = "[{0} {1} {2}] {3}".format(
                self.clock(), self.tool_name, level, part
            )
            if self.color and color_code:
                rendered = "\033[{0}m{1}\033[0m".format(color_code, rendered)
            self.stream.write(rendered + "\n")
        self.stream.flush()

    def info(self, message):
        """Write an informational message."""
        self.line("INFO", message)

    def prompt(self, message):
        """Write a prompt."""
        self.line("PROMPT", message, "36")

    def menu(self, question, options):
        """Write one labeled question followed by unprefixed choices.

        Args:
            question (str): Menu question shown as a prompt.
            options (list[str]): Display lines for the choices.
        """
        self.prompt(question)
        for option in options:
            rendered = "  " + str(option)
            if self.color:
                rendered = "\033[36m" + rendered + "\033[0m"
            self.stream.write(rendered + "\n")
        self.stream.flush()

    def warn(self, message):
        """Write a warning."""
        code = "38;5;208" if "256color" in os.environ.get("TERM", "") else "33"
        self.line("WARN", message, code)

    def error(self, message):
        """Write an actionable error."""
        self.line("ERROR", message, "31")

    def success(self, message):
        """Write the final successful outcome."""
        self.line("SUCCESS", message, "32")

    def status(self, message):
        """Classify an existing installer callback message."""
        lowered = str(message).lower()
        if lowered.startswith("installed "):
            self.success(message)
        elif "cancelled" in lowered or "canceled" in lowered:
            self.info(message)
        elif any(word in lowered for word in ("unknown ", "cannot ", "does not exist", "not a directory", "conflicting")):
            self.warn(message)
        else:
            self.info(message)

    def input_function(self, prompt):
        """Display a contract prompt and read one answer."""
        text = prompt.rstrip()
        default_match = re.search(r"\[(Y/n|y/N)\]", text)
        if default_match:
            default_name = "Y" if default_match.group(1) == "Y/n" else "n"
            text = text.rstrip(": ") + " (default: " + default_name + "):"
        self.prompt(text)
        try:
            reader = raw_input
        except NameError:
            reader = input
        return reader("")


def run_installer(tool_name, installer):
    """Run one standalone installer with contract output.

    Args:
        tool_name (str): Catalog command name.
        installer (callable): Installer accepting input and output callbacks.

    Returns:
        int: Zero on completion or cancellation, one after an error.
    """
    output = TerminalOutput(tool_name)
    error_output = TerminalOutput(tool_name, sys.stderr)
    output.info("Checking installer inputs and destinations...")
    output.info("Installing selected agent workspace files...")
    try:
        installer(input_function=output.input_function, output_function=output.status)
        return 0
    except (KeyboardInterrupt, EOFError):
        output.info("Installation cancelled; files already written, if any, were left in place.")
        return 0
    except Exception as error:
        error_output.error(
            "Installation failed: {0}. Some earlier changes may remain; correct the error and retry.".format(error)
        )
        return 1
