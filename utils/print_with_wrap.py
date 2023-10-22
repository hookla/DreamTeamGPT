import textwrap


def print_with_wrap(text: str, wrap_length: int = 180):
    lines = text.split("\n")
    for line in lines:
        wrapped_text = textwrap.wrap(line, wrap_length)
        for segment in wrapped_text:
            print(segment)
