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
sys.path.insert(0, os.path.abspath('..'))

def setup(app):
    app.add_css_file("my-styles.css")


# -- Project information -----------------------------------------------------

project = u'ECAS Notebook Documentation'
copyright = u'2020, ECASLab'
author = 'Manos'

# The full version, including alpha/beta/rc tags
release = '0.1'


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
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

sphinx_gallery_conf = {
    'examples_dirs': ["examples"],
    'gallery_dirs': ["autoexamples"],
    'plot_gallery': 'False',
}

html_sidebars = {'**': ['side-bar.html', 'searchbox.html'], 'index': [], }
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

# Name of the master document
master_doc = 'index'

# Other configuration specific for extensions
process_examples = True

nbsphinx_allow_errors = True
nbsphinx_execute = 'never'
