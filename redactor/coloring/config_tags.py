def config_tags(text_widget, language):
    with open('settings/{}_keywords.json'.format(language)) as data_file:
        keywords = eval(data_file.read())
    for k, v in keywords.items():
        text_widget.tag_config(k, foreground=v)
    text_widget.tag_config('blank', foreground='black')
    return keywords
