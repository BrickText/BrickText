import os


def config_tags(text_widget, language):
    with open(os.path.dirname(__file__) +
              '/../../settings/{}_keywords.json'
              .format(language)) as data_file:
        keywords = eval(data_file.read())
    for k, v in keywords.items():
        text_widget.tag_config(k, foreground=v)
    with open(os.path.dirname(__file__) +
              '/../../settings/common_keywords.json') as data_file:
        common_keywords = eval(data_file.read())
    for k, v in common_keywords.items():
        text_widget.tag_config(k, foreground=v)
    text_widget.tag_config('blank', foreground='black')
    return keywords


def reset_tags(text_widget, language, prev_language=None):
    if prev_language:
        with open(os.path.dirname(__file__) +
                  '/../../settings/{}_keywords.json'
                  .format(prev_language)) as data_file:
            keywords = eval(data_file.read())
        for k, v in keywords.items():
            text_widget.tag_delete(k)

    return config_tags(text_widget, language)
