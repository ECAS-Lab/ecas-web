import sphinx_bootstrap_theme
import os
import sys
import sphinx_gallery
sys.path.insert(0, os.path.abspath('..'))


def setup(app):
    app.add_stylesheet("my-styles.css")


project = u'Ophidia'
copyright = u'2020, CMCC Foundation'
author = 'Manos'
extensions = ['nbsphinx', 'sphinx_gallery.gen_gallery', 'sphinx.ext.autosectionlabel']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

html_static_path = ['_static']

sphinx_gallery_conf = {
    'examples_dirs': ["examples"],
    'gallery_dirs': ["autoexamples"],
}

html_sidebars = {'**': ['side-bar.html', 'searchbox.html'], 'index': [], }
html_theme_options = {
    'navbar_site_name': "Sections",

    'globaltoc_depth': 1,

    'globaltoc_includehidden': "true",
}

process_examples = True

master_doc = 'index'
nbsphinx_allow_errors = True
