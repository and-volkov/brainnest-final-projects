from time import monotonic
import logging

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Button, Header, Footer, Static, Input

log_level = logging.INFO
logger = logging.getLogger("main")
logging.basicConfig(
    filename="countdown.log",
    encoding="utf-8",
    level=log_level,
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
)


class TimeDisplay(Static):
    """A widget to display elapsed time."""

    start_time = reactive(monotonic)
    time = reactive(60.0)
    total = reactive(60.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(
            1 / 60, self.update_time, pause=True
        )

    def update_time(self) -> None:
        """Method to update time to current."""
        self.time = self.total - (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self):
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total -= monotonic() - self.start_time
        self.time = self.total

    def reset(self):
        """Method to reset the time display to zero."""
        self.total = 60.0
        self.time = 60.0


class TimeInput(Input):
    """A widget to input a time."""

    def __init__(self, time_display: TimeDisplay):
        super().__init__()
        self.placeholder = "Enter time in seconds"
        self.time_display = time_display

    def on_key(self, event: Input) -> None:
        """Event handler called when a key is pressed."""
        if event.key == "enter":
            try:
                float(self.value)
            except ValueError:
                self.value = "60.0"
            if float(self.value) < 0:
                self.value = "60.0"
            self.time_display.set_total(float(self.value))
            self.remove()
        elif event.key == "escape":
            self.remove()
        else:
            super().on_key(event)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.time_display.set_total(60.0)
        self.focus()


class Countdown(Static):
    """A countdown widget."""

    def __init__(self):
        super().__init__()
        self.time_display = TimeDisplay()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == "start":
            time_display.start()
            self.add_class("started")
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        """Create child widgets of a countdown."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield self.time_display

    def set_total(self, total: float) -> None:
        """Method to set the total time."""
        self.time_display.total = total
        self.time_display.time = total


class CountdownApp(App):
    """A Textual app to manage countdowns."""

    CSS_PATH = "countdown.css"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_countdown", "Add"),
        ("r", "remove_countdown", "Remove"),
        ("i", "set_interval", "Set interval"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()

    def focus(self) -> None:
        """Event handler called when widget gains focus."""
        self.add_class("focused")

    def action_add_countdown(self) -> None:
        """An action to add a timer."""
        new_countdown = Countdown()
        try:
            self.query_one("#timers").mount(new_countdown)
        except NoMatches:
            self.mount(Container(new_countdown, id="timers"))
        new_countdown.scroll_visible()

    def action_remove_countdown(self) -> None:
        """Called to remove a timer."""
        timers = self.query("Countdown")
        if timers:
            timers.last().remove()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_set_interval(self) -> None:
        """An action to set the interval."""
        try:
            last_timer = self.query("Countdown").last()
        except NoMatches:
            self.action_add_countdown()
        last_timer = self.query("Countdown").last()
        new_input = TimeInput(last_timer)
        try:
            self.query_one("#timeinput").mount(new_input)
        except NoMatches:
            self.mount(Container(new_input, id="timeinput"))


if __name__ == "__main__":
    try:
        app = CountdownApp()
        app.run()
    except Exception as e:
        logger.exception(e)
        pass
