from collections import defaultdict
from typing import Any, Dict, Iterator, List, Tuple

from sphinx.domains import Index, IndexEntry
from sphinx.domains.javascript import JavaScriptDomain

from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.console import bold

logger = logging.getLogger(__name__)
prefix = bold(__('Sphinx-ext-jsindices: '))

# IndexEntry = NamedTuple('IndexEntry', [('name', str),
#                                        ('subtype', int),
#                                        ('docname', str),
#                                        ('anchor', str),
#                                        ('extra', str),
#                                        ('qualifier', str),
#                                        ('descr', str)])


class JavaScriptBaseIndex(Index):

    @classmethod
    def configure(cls, config):
        options = config.jsindices_options
        msg = "configure indices"
        logger.info(prefix + msg)

        # get options and set defaults
        cls.use_short_names = options.get("short_names", False)
        cls.collapse = options.get("collapse", False)

class JavaScriptModuleIndex(JavaScriptBaseIndex):
    """A custom index that creates a JavaScript module matrix."""

    name = "modindex"
    localname = "JavaScript Module Index"
    shortname = "JS Modindex"

    def generate(self, docnames=None):
        msg = "generate module index"
        logger.info(prefix + msg)

        content = defaultdict(list)

        modules = {name: (dispname, typ, docname, anchor)
                   for name, dispname, typ, docname, anchor, _
                   in self.domain.get_objects() if typ == "module"}

        for module in sorted(modules):
            dispname, typ, docname, anchor = modules[module]
            content[dispname[0].upper()].append(
                (dispname, 0, docname, anchor, docname, '', typ))

        content = sorted(content.items())
        return content, self.collapse


class JavaScriptClassIndex(JavaScriptBaseIndex):
    """A custom index that creates a JavaScript class matrix."""

    name = "classindex"
    localname = "JavaScript Class Index"
    shortname = "JS Classindex"

    def generate(self, docnames=None):
        msg = "generate class index"
        logger.info(prefix + msg)

        content = defaultdict(list)

        classes = {name: (dispname, typ, docname, anchor)
                   for name, dispname, typ, docname, anchor, _
                   in self.domain.get_objects() if typ == "class"}

        for _class in sorted(classes):
            dispname, typ, docname, anchor = classes[_class]
            content[dispname[0].upper()].append(
                (dispname, 0, docname, anchor, docname, '', typ))

        content = sorted(content.items())
        return content, self.collapse


class JavaScriptObjectIndex(JavaScriptBaseIndex):
    """A custom index that creates a JavaScript module, class and namespace matrix (nested)."""

    name = "index"
    localname = "JavaScript Object Index"
    shortname = "JS index"

    def generate(self, docnames=None):
        msg = "generate object"
        logger.info(prefix + msg)

        content = defaultdict(list)

        object_filter = ["class", "namespace", "module"]
        objects = {name: (dispname, typ, docname, anchor)
                   for name, dispname, typ, docname, anchor, _
                   in self.domain.get_objects() if typ in object_filter }

        prev_modname = ""
        num_toplevels = 0
        for module in sorted(objects):
            dispname, typ, docname, anchor = objects[module]
            subtype = 0
            modname = dispname.split(".")[0]
            entries = content.setdefault(modname[0].lower(), [])
            if dispname != modname:
                # it's an object of a module
                # and even the first object - make parent a group head
                if prev_modname == dispname and entries:
                    last = entries[-1]
                    entries[-1] = IndexEntry(last[0], subtype, last[2], last[3],
                                            last[4], last[5], last[6])
                elif not dispname.startswith(prev_modname):
                    # object without parent in list, add dummy entry
                    entries.append(IndexEntry(dispname, subtype, '', '', '', '', ''))
                subtype = 2
                if self.use_short_names:
                    dispname = dispname.split(".")[-1]
            else:
                num_toplevels += 1
                subtype = 1

            entries.append(IndexEntry(dispname, subtype, docname, anchor,docname, '', typ))
            prev_modname = modname

        # apply heuristics when to collapse index at page load:
        # only collapse if number of toplevel modules is larger than
        # number of objects (same logic in python domain)
        # update: customize behaviour with collapse option
        # collapse = len(objects) - num_toplevels < num_toplevels

        # sort by first letter
        sorted_content = sorted(content.items())
        return sorted_content, self.collapse

def configure_indices(app, config):
    JavaScriptBaseIndex.configure(config)


def setup(app) -> Dict[str, Any]:
    app.add_config_value('jsindices_options', {}, 'env')

    app.add_index_to_domain("js", JavaScriptObjectIndex)
    app.add_index_to_domain("js", JavaScriptModuleIndex)
    app.add_index_to_domain("js", JavaScriptClassIndex)

    app.connect("config-inited", configure_indices)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
