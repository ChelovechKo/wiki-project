import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


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


def convert_markdown_to_html(text):
    """
    Convert markdown text into html and return.
    Supporting headings, boldface text, unordered lists, links, and paragraphs
    """
    def replace_unordered_lists(text):
        ul_items = re.findall(r'^[*-+]\s+.+', text, re.MULTILINE)

        if ul_items:
            html_list = '<ul>\n'
            for item in ul_items:
                item_text = re.sub(r'^[*-+]\s+', '', item)
                html_list += f'  <li>{item_text}</li>\n'
            html_list += '</ul>'

            # Вставляем HTML-код списка в текст, но только там, где он начинается
            text = re.sub(r'((?:^[*-+]\s+.+\n?)+)', html_list, text, flags=re.MULTILINE)

        return text

    # Headers
    text = re.sub(r'### (.+)', r'<h3>\1</h3>', text)
    text = re.sub(r'## (.+)', r'<h2>\1</h2>', text)
    text = re.sub(r'# (.+)', r'<h1>\1</h1>', text)

    # Unordered lists
    text = replace_unordered_lists(text)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    # Paragraph
    paragraphs = text.strip().split("\n\n")
    text = ''.join([f'<p>{p.strip()}</p>\n' for p in paragraphs])
    return text