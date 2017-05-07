"""TeX Builder Module
version: 1.0.0
author: Long Gong
email: long.github@gmail.com
"""

_IMPORT_ERROR_MSG = u"{0} was not detected, please run \
'pip install {0}' to install it."

try:
    from jinja2 import Environment
    from jinja2 import FileSystemLoader
except ImportError:
    print(_IMPORT_ERROR_MSG.format("jinja2"))
    exit(1)


class TeXBuilder(object):
    """Simple class for TeX Builder"""

    _TEMPLATE_KEY_NOT_FOUND = "No template with key \"{0}\" was found," \
                              "a random template will be used instead."

    def __init__(self, template_dir, templates, default="default"):
        self.template_dir = template_dir
        self.templates = templates

        self.selected_template = None
        self.set_template(default)

    def set_template(self, template_key, template_dir=None):
        if template_dir is None:
            pass
        else:
            self.template_dir = template_dir
        if self.templates.get(template_key, None) is None:
            print(TeXBuilder._TEMPLATE_KEY_NOT_FOUND.format(template_key))
            for key in self.templates:
                self.selected_template = self.templates[key]
                break
        else:
            self.selected_template = self.templates[template_key]

    def make_tex(self, arguments):
        j2_env = Environment(loader=FileSystemLoader(self.template_dir),
                             trim_blocks=True)
        return j2_env.get_template(self.selected_template).render(
            arguments
        )




