from wtforms import BooleanField
from wtforms.widgets import Input


class CancelInput(Input):
    """
    Renders a cancel button.
    The field's label is used as the text of the cancel button instead of the
    data on the field.
    """
    input_type = 'button'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('value', field.label.text)
        return super(CancelInput, self).__call__(field, **kwargs)


class CancelField(BooleanField):
    """
    Represents an ``<input type="button">``.  This allows checking if a given
    cancel button has been pressed.
    """
    widget = CancelInput()
