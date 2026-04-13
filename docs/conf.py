from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath("../libs/spm_slang/src"))

project = "spm.slang"
author = "Fangjun Zhou"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

source_suffix = {
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"

myst_enable_extensions = [
    "colon_fence",
]

autodoc_typehints = "description"
autodoc_mock_imports = ["slangpy"]
