from django import template
import re

register = template.Library()

@register.filter
def youtube_id(url):
    regex = r"(?:v=|be/|embed/)([\w-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else ""