# sphinx-ext-jsindices
Extend Sphinx with some JavaScript indices.

# Installation
This extension is currently not available on PyPI. Use pip instead.

Install via pip

```code
pip install git+https://github.com/nemetris/sphinx-ext-jsindices.git
```

# Usage
Activate the extension in your Sphinx configuration file ```conf.py```:

```code
extensions = [
    'sphinx_ext_jsindices'
]
```

At ```sphinx-build``` process, this will automatically generate html index pages
which contain lists of all documented JavaScript objects like modules, classes and namespaces.
Use the ```:ref:``` role to link those pages:

```code
Indices And Tables
==================

* :ref:`JavaScript Object Index <js-index>`
* :ref:`JavaScript Module Index <js-modindex>`
* :ref:`JavaScript Class and Namespace Index <js-classindex>`
```

# Options

Define a dictionary called ```jsindices_options``` to adjust the default options

```python
# default options
jsindices_options = {
    "short_names": False,
    "collapse": None,
}
```

| **Option**  | Values                                                                                                 |      Description      |
|:------------|:-------------------------------------------------------------------------------------------------------|:---------------------:|
| short_names | Removes all prefixes and just displays the short name of a class, function or whatever                 |   ```True/False```    |
| collapse    | Always collapse all entries on page load if set to ```True```. Default is ```None``` (python index behaviour). | ```True/False/None``` |
