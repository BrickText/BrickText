import re

from coloring.config_tags import config_tags


class Coloring:
    def __init__(self, text_editor, language):
        self.root = text_editor.get_root()
        self.text_widget = text_editor.get_text_panel()
        self.keywords = config_tags(self.text_widget, language)
        self.pattern = r"\w+"
        self.root.after(200, self.findall)

    def coloring(self, indices):
        for f, l in indices:
            word = self.text_widget.get(f, l)
            if word in self.keywords.keys():
                self.text_widget.tag_remove('blank', f, l)
                self.text_widget.tag_add(word, f, l)
            else:
                for k, _ in self.keywords.items():
                    self.text_widget.tag_remove(k, f, l)
                self.text_widget.tag_add('blank', f, l)

    def findall(self, start="1.0", end="end"):
        start = self.text_widget.index(start)
        end = self.text_widget.index(end)
        string = self.text_widget.get(start, end)

        indices = []
        if string:
            matches = re.finditer(self.pattern, string)
            for match in matches:
                match_start = self.text_widget.index("%s+%dc" %
                                                     (start, match.start()))
                match_end = self.text_widget.index("%s+%dc" %
                                                   (start, match.end()))
                indices.append((match_start, match_end))

        self.coloring(indices)

        self.root.after(200, self.findall)
