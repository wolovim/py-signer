from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Input, RadioButton, RadioSet, Footer

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
        yield Input(placeholder="value", classes="type-input")
        with RadioSet():
            for t in VALID_TYPES:
                yield RadioButton(t, id=t)


class Domain(Static):
    """EIP-712 Domain input"""

    ## TODO: show one field at a time? input field, description, buttons: save/skip

    # eip712_domain_map = {
    #     "name": {"name": "name", "type": "string"},
    #     "version": {"name": "version", "type": "string"},
    #     "chainId": {"name": "chainId", "type": "uint256"},
    #     "verifyingContract": {"name": "verifyingContract", "type": "address"},
    #     "salt": {"name": "salt", "type": "bytes32"},
    # }

    OUTPUT_EXAMPLE = """
    {
        "name": "Ether Mail",
        "version": "1",
        "chainId": 1,
        "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
        "salt": b"decafbeef",
    }"""

    def compose(self):
        yield Static("Domain Data", classes="title")
        with Horizontal(classes="domain-container"):
            with Vertical(classes="domain-input-form"):
                with Horizontal(classes="domain-input-container"):
                    yield Input(
                        placeholder="name (e.g., Ether Mail)", classes="domain-input"
                    )
                    yield RadioSet(
                        RadioButton("string", id="domain-name-type", value=True)
                    )
                with Horizontal(classes="domain-input-container"):
                    yield Input(placeholder="version (e.g., 1)", classes="domain-input")
                    yield RadioSet(
                        RadioButton("string", id="domain-version-type", value=True)
                    )
                with Horizontal(classes="domain-input-container"):
                    yield Input(placeholder="chainId (e.g., 1)", classes="domain-input")
                    yield RadioSet(
                        RadioButton("uint256", id="domain-chainid-type", value=True)
                    )
                with Horizontal(classes="domain-input-container"):
                    yield Input(
                        placeholder="verifyingContract (e.g., 0xCcCCc...)",
                        classes="domain-input",
                    )
                    yield RadioSet(
                        RadioButton("address", id="domain-contract-type", value=True)
                    )
                with Horizontal(classes="domain-input-container"):
                    yield Input(
                        placeholder="salt (e.g., b'decafbeef')", classes="domain-input"
                    )
                    yield RadioSet(
                        RadioButton("bytes32", id="domain-salt-type", value=True)
                    )
            with Vertical(classes="output-container"):
                yield Static(self.OUTPUT_EXAMPLE, classes="output-body")


class CustomTypes(Static):
    """EIP-712 structured data"""

    TYPES_EXAMPLE_STRING = """{ "Person": [ {"name": "name", "type": "string"}, {"name": "wallet", "type": "address"}, ], "Mail": [ {"name": "from", "type": "Person"}, {"name": "to", "type": "Person"}, {"name": "contents", "type": "string"}, ] }"""
    TYPES_EXAMPLE_FORMATTED = """
    {
        "Person": [
            {"name": "name", "type": "string"},
            {"name": "wallet", "type": "address"},
        ],
        "Mail": [
            {"name": "from", "type": "Person"},
            {"name": "to", "type": "Person"},
            {"name": "contents", "type": "string"},
        ],
    }"""

    def compose(self):
        yield Static("Custom Types", classes="title")
        yield Input(placeholder="xyz", classes="types-input")
        with Vertical(classes="output-container"):
            yield Static(
                f"Your types: {self.TYPES_EXAMPLE_FORMATTED}", classes="output-body"
            )
        yield Static(id="fields")

    def on_mount(self):
        self.query_one("#fields").mount(Field())


class Signer(App):
    """Builds EIP-712 compliant signed messages"""

    CSS_PATH = "main.tcss"
    BINDINGS = [
        ("ctrl+n", "add_field", "Add Field"),
        ("ctrl+r", "remove_field", "Remove Last Field"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def compose(self):
        yield Footer()
        yield Domain()
        yield CustomTypes()

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

# msg_types = {
#     ...     "Person": [
#     ...         {"name": "name", "type": "string"},
#     ...         {"name": "wallet", "type": "address"},
#     ...     ],
#     ...     "Mail": [
#     ...         {"name": "from", "type": "Person"},
#     ...         {"name": "to", "type": "Person"},
#     ...         {"name": "contents", "type": "string"},
#     ...     ],
#     ... }

#     >>> # the data to be signed
#     >>> msg_data = {
#     ...     "from": {
#     ...         "name": "Cow",
#     ...         "wallet": "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826",
#     ...     },
#     ...     "to": {
#     ...         "name": "Bob",
#     ...         "wallet": "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB",
#     ...     },
#     ...     "contents": "Hello, Bob!",
#     ... }

# TODO: video tutorial
