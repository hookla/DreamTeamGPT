import textwrap


def pretty_print_with_wrap(text: str, wrap_length: int = 180):
    wrapped_text = textwrap.fill(text, wrap_length)
    print(wrapped_text)
