from textual.reactive import reactive
from textual.widgets import Static


class LabelValidation(Static):

    error_label = reactive('')

    def update_text(self, text: str) -> None:
        self.error_label = text
        self.update(f"{self.error_label}")
