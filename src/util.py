# Standard library
import logging

logger = logging.getLogger(__name__)  # put this in each file


def loop_replace(text_str="", replacements=[""]):
    """Does str.replace() for a list of strings.
    Args:
        text_str (str): text to remove from
        replacements (list, optional): list of strings to remove. Defaults to [""].
    Returns:
        string: text_str without the strings in replacements
    """

    if replacements != [""]:
        for i in replacements:
            text_str = text_str.replace(i, "")
    return text_str


def seconds_but_readable(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)
