from textual.app import App
from textual.containers import Horizontal
from textual.widgets import Static, Input, RadioButton, RadioSet, Header, Footer


VALID_TYPES = [
    "address",
    "boolean",
    "string",
    "bytes",
    "int8",
    "int256",
    "uint8",
    "uint256",
]


class Field(Static):
    """Individual type input field"""

    def compose(self):
        with Horizontal():
            yield Input(placeholder="value", classes="type-input")
            with RadioSet():
                for t in VALID_TYPES:
                    yield RadioButton(t, id=t)


class Signer(App):
    """Builds EIP-712 compliant signed messages"""

    CSS_PATH = "main.tcss"
    BINDINGS = [
        ("ctrl+n", "add_field", "Add Field"),
        ("ctrl+r", "remove_field", "Remove Last Field"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def compose(self):
        yield Header()
        yield Footer()
        yield Static(id="fields")

    def on_mount(self):
        self.query_one("#fields").mount(Field())

    def on_radio_set_changed(self, event):
        print(event.pressed.label)
        print(event.radio_set.pressed_index)

    def action_add_field(self):
        self.query_one("#fields").mount(Field())

    def action_remove_field(self):
        fields = self.query(Field)
        if fields:
            fields.last().remove()

    def action_quit(self):
        self.exit()


if __name__ == "__main__":
    app = Signer()
    app.run()

# TODO: video tutorial
