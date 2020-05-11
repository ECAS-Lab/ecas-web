# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sphinx_bootstrap_theme
import os
import sys
import sphinx_gallery
# sys.path.insert(0, "C:\\Users\\user\\Desktop\\sphinx_third\\results")
# sys.path.insert(0, os.getcwd())
# sys.path.insert(0, os.path.join(os.getcwd(), "results"))
sys.path.insert(0, os.path.abspath('..'))
# sys.path.insert(0, os.path.join(os.path.abspath('..'), "results"))
# sys.path.insert(0, os.path.join(os.path.abspath('..'), "results", "examples"))
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# sys.path.insert(0, os.path.join(os.path.abspath('..'), "results"))
# sys.path.insert(0, os.path.join(os.path.abspath('..'), "results", "examples"))
# print(os.path.join(os.path.abspath('..'), "results"))


def setup(app):
    app.add_stylesheet("my-styles.css") # also can be a full URL
    # app.add_stylesheet("ANOTHER.css")
    # app.add_stylesheet("AND_ANOTHER.css")

# -- Project information -----------------------------------------------------

project = 'notebooks_documentation'
copyright = '2020, Manos'
author = 'Manos'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['nbsphinx', 'sphinx_gallery.gen_gallery', 'sphinx.ext.autosectionlabel']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

sphinx_gallery_conf   = {
     'examples_dirs': ["examples"],   # path to your example scripts
     'gallery_dirs': ["autoexamples"],
}

# example_gallery_config  = {
#      'examples_dirs': [os.path.join(os.getcwd(), "examples")],   # path to your example scripts
#      'gallery_dirs': ["autoexamples", os.path.join(os.path.abspath('..'), "results", "autoexamples")]
# }

html_sidebars = {'**': ['side-bar.html', 'searchbox.html'],  'index': [],}
html_theme_options = {
    'navbar_site_name': "Sections",

    # Global TOC depth for "site" navbar tab. (Default: 1)
    'globaltoc_depth': 1,

    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    'globaltoc_includehidden': "true",
}


process_examples = True


master_doc = 'index'
nbsphinx_allow_errors = True
