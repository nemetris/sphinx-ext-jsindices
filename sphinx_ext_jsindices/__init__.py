from collections import defaultdict
from typing import Any, Dict, Iterator, List, Tuple

from sphinx.domains import Index
from sphinx.domains.javascript import JavaScriptDomain

class JavaScriptModuleIndex(Index):
    """A custom index that creates a JavaScript module matrix."""

    name = "modindex"
    localname = "JavaScript Module Index"
    shortname = "JS Modindex"

    def generate(self, docnames=None):
        content = defaultdict(list)

        modules = {name: (dispname, typ, docname, anchor)
                   for name, dispname, typ, docname, anchor, _
                   in self.domain.get_objects() if typ == "module"}

        for dispname, typ, docname, anchor in modules.values():
            content[dispname[0].upper()].append(
                (dispname, 0, docname, anchor, docname, '', typ))

        content = sorted(content.items())
        return content, True


class JavaScriptClassIndex(Index):
    """A custom index that creates a JavaScript class matrix."""

    name = "classindex"
    localname = "JavaScript Class Index"
    shortname = "JS Classindex"

    def generate(self, docnames=None):
        content = defaultdict(list)

        modules = {name: (dispname, typ, docname, anchor)
                   for name, dispname, typ, docname, anchor, _
                   in self.domain.get_objects() if typ == "class"}

        for dispname, typ, docname, anchor in modules.values():
            content[dispname[0].upper()].append(
                (dispname, 0, docname, anchor, docname, '', typ))

        content = sorted(content.items())
        return content, True


class JavaScriptObjectIndex(Index):
    """A custom index that creates a JavaScript module, class and namespace matrix."""

    name = "index"
    localname = "JavaScript Object Index"
    shortname = "JS index"

    def generate(self, docnames=None):
        content = defaultdict(list)

        object_filter = ["class", "namespace", "module"]
        objects = {name: (dispname, typ, docname, anchor)
                   for name, dispname, typ, docname, anchor, _
                   in self.domain.get_objects() if typ in object_filter }

        for dispname, typ, docname, anchor in objects.values():
            content[dispname[0].upper()].append(
                (dispname, 0, docname, anchor, docname, '', typ))

        content = sorted(content.items())
        return content, True


def setup(app) -> Dict[str, Any]:
    app.add_index_to_domain("js", JavaScriptObjectIndex)
    app.add_index_to_domain("js", JavaScriptModuleIndex)
    app.add_index_to_domain("js", JavaScriptClassIndex)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
