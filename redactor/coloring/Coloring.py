import re

from coloring.config_tags import config_tags, reset_tags


class Coloring:
    def __init__(self, text_editor, language):
        self.root = text_editor.get_root()
        self.text_widget = text_editor.get_text_panel()
        self.language = language
        self.keywords = config_tags(self.text_widget, language)
        self.pattern = r"\w+\(|\w+|([\"'])(?:(?=(\\?))\2.)*?\1"

    def reset_tags(self, new_language):
        self.keywords = reset_tags(self.text_widget, new_language,
                                   self.language)

    def coloring(self, indices):
        for f, l in indices:
            word = self.text_widget.get(f, l)
            pos = word.find('(')
            fs = f.split('.')
            ls = l.split('.')
            w = ''
            if pos > 0:
                w = word[:-(len(word) - pos)]
            if word in self.keywords.keys():
                self.text_widget.tag_remove('blank', f, l)
                self.text_widget.tag_add(word, f, l)
            elif w in self.keywords.keys():
                self.text_widget.tag_remove('blank', f, l)
                self.text_widget\
                    .tag_add(w, f, '{}.{}'.format(fs[0], int(fs[1]) + pos))
            else:
                for k, _ in self.keywords.items():
                    self.text_widget.tag_remove(k, f, l)
                pos = word.find('(')
                if pos > 0:
                    self.text_widget.tag_remove('blank', f, l)
                    self.text_widget\
                        .tag_add('functions', f,
                                 '{}.{}'.format(fs[0], int(fs[1]) + pos))
                elif word[0] == '\'':
                    if word[-1] == '\'':
                        self.text_widget.tag_remove('blank', f, l)
                        self.text_widget\
                            .tag_add('string',
                                     '{}.{}'.format(fs[0], int(fs[1]) + 1),
                                     '{}.{}'.format(ls[0], int(ls[1]) - 1))
                elif word[0] == '"':
                    if word[-1] == '\"':
                        self.text_widget.tag_remove('blank', f, l)
                        self.text_widget\
                            .tag_add('string',
                                     '{}.{}'.format(fs[0], int(fs[1]) + 1),
                                     '{}.{}'.format(ls[0], int(ls[1]) - 1))
                else:
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
