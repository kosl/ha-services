from __future__ import annotations

import sys

from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich.panel import Panel
from rich.pretty import Pretty
from rich.text import Text


class PanelPrinter:
    def __init__(
        self,
        *,
        HighlighterClass=ReprHighlighter,
        border_style='bright_yellow',
        padding=(2, 5),
        console=None,
    ):
        if HighlighterClass is not None:
            self.highlighter = HighlighterClass()
        else:
            self.highlighter = None

        self.HighlighterClass = HighlighterClass
        self.border_style = border_style
        self.padding = padding
        self.console = console or Console()
        self.console.print()

    def print_panel(self, *, content, title, border_style=None):
        self.console.print(
            Panel(
                self.highlight(content),
                title=title,
                border_style=border_style or self.border_style,
                expand=False,
                padding=self.padding,
            )
        )
        self.console.print()

    def highlight(self, content):
        if not isinstance(content, (str, Text)):
            content = Pretty(content)
        elif self.highlighter:
            content = self.highlighter(content)
        return content


def human_error(
    message: str,
    *,
    title='[red]Error',
    exit_code=None,
    exception: BaseException | None = None,
    HighlighterClass=ReprHighlighter,
    border_style='bright_red',
    padding=(2, 5),
    console=None,
):
    """
    Print a message in a Panel.
    Optional:
        - print traceback first
        - Exit with: sys.exit(exit_code)
    """
    if console is None:
        use_stderr = exception is not None
        console = Console(stderr=use_stderr)

    console.print('\n')

    if exception is not None:
        assert isinstance(exception, BaseException), f'Not a exception: {exception!r}'
        console.print_exception(show_locals=True)

    console.print()

    pp = PanelPrinter(HighlighterClass=HighlighterClass, border_style=border_style, padding=padding, console=console)
    pp.print_panel(content=message, title=title)

    if exit_code is not None:
        sys.exit(exit_code)
