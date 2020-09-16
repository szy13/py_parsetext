import re


class Parser:
    def __init__(self, pattern):
        self.pattern = pattern

    @property
    def tags(self):
        return re.findall(r'<(.+?)>', self.pattern, re.IGNORECASE)

    @property
    def tags_clear(self):
        return [tag.replace('?', '') for tag in self.tags]

    @property
    def formatted(self):
        pattern = self.pattern
        pattern = re.sub(r'\[(.+?)\]', r'(?:\1)', pattern)

        for tag in self.tags:
            optional = '?' if tag.endswith('?') else ''
            if pattern.find(f'<{tag}>') == 0:
                pattern = re.sub('<' + re.escape(tag) + r'>\s+', r'(?:(.+?)[ ]+)' + optional, pattern)
            else:
                pattern = re.sub(r'\s+<' + re.escape(tag) + '>', r'(?:[ ]+(.+?))' + optional, pattern)

        return pattern

    def match(self, text):
        tags = self.tags
        clear_tags = self.tags_clear

        match = re.match(f'^{self.formatted}$', text, re.DOTALL | re.IGNORECASE)

        if not match:
            return False

        return dict(zip(clear_tags, match.groups()))
