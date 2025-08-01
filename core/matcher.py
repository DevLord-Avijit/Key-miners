import re
import asyncio

def compile_patterns(patterns):
    """
    Compiles regex patterns for faster matching.
    """
    return {name: re.compile(pattern) for name, pattern in patterns.items()}

async def match_patterns(text, compiled_patterns):
    """
    Asynchronously scans the text using precompiled regex patterns.

    Args:
        text (str): The input string to scan.
        compiled_patterns (dict): Dictionary of {pattern_name: compiled_regex}

    Returns:
        list of tuples: [(pattern_name, matched_string), ...]
    """
    results = []

    for name, pattern in compiled_patterns.items():
        matches = pattern.findall(text)
        for match in matches:
            if isinstance(match, tuple):
                match = ''.join(match)
            results.append((name, match))

    return results
