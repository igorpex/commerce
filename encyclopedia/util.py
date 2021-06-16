import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from markdown2 import Markdown


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    except UnicodeDecodeError:
        try:
            f = default_storage.open(f"entries/{title}.md")
            return f.read().decode ('Windows-1251')
        except Exception as exc:
            return f'Text decoding error: {exc}'
    except Exception as exc:
        return f'Error: {exc}'


def get_html_entry(title):
    md = get_entry(title)
    if md == None:
        return "Error reading file"
    markdowner = Markdown()
    return markdowner.convert(md)

def search(q):
    entries = list_entries()
    """
    Provides filtered list of entries
    """
    def filter_search (entry):
        if q.lower() in entry.lower():
            return True
        else:
            return False

    return filter(filter_search, entries)