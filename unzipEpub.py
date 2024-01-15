# open up the pg507-images-3.epub file and extract all the xhtml files

import zipfile
import os
import re

# open the epub file
epub = zipfile.ZipFile('pg507-images-3.epub', 'r')

# extract all the xhtml files
epub.extractall('pg507-images-3')

# close the epub file
epub.close()

