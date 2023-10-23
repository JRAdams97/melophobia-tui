from textual.reactive import reactive
from textual.widgets import Static


class SubmitLabel(Static):
    text = reactive('')

    def update_text(self, is_valid_form: bool) -> None:
        if is_valid_form:
            self.text = 'Form successfully submitted!'

        else:
            self.text = 'Validation errors found!'

        self.update(f"{self.text}")
