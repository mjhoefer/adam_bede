# this script should read through the content.opf file and create a list of all the xhtml files, one per chapter, then print out the list

import zipfile
import os
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# open the content.opf file
content = open('pg507-images-3/OEBPS/content.opf', 'r')

# read the content.opf file
opf_content = content.read()


def get_chapter_files(opf_xml):
    # Parse the XML
    root = ET.fromstring(opf_xml)

    # Namespace handling (if the XML uses namespaces)
    namespaces = {
        'opf': 'http://www.idpf.org/2007/opf'
    }

    # Regular expression to match chapter files (e.g., h-1, h-2, etc.)
    chapter_pattern = re.compile(r'h-\d+')

    # Find all <item> elements in the <manifest> that are XHTML (chapters)
    chapter_files = []
    for item in root.findall('.//opf:item', namespaces):
        if 'application/xhtml+xml' in item.get('media-type'):
            href = item.get('href')
            if chapter_pattern.search(href):  # Match files with 'h-#' pattern
                chapter_files.append(href)

    return chapter_files

# Extract chapter files
chapter_files = get_chapter_files(opf_content)

# get the path to each chapter file
chapter_files = [os.path.join('pg507-images-3/OEBPS', chapter_file) for chapter_file in chapter_files]


# function that takes in the content of a <p> tag and returns a list of all the quotes in that tag
def get_quotes(paragraph):
    # create a list to hold the quotes
    quotes = []
    # use regular expressions to find all the quotes
    # Regex to find text within quotes
    quotes_pattern = r'“[^”]*”'

    # Find all occurrences of the pattern
    quotes = re.findall(quotes_pattern, paragraph)
    return quotes
    


# for each chapter file, open it and find any quotes within a <p> tag
# for each quote, print it out
for i, chapter_file in enumerate(chapter_files):
    # if chapter file is not the second one, skip
    if i != 1:
        continue
    with open(chapter_file, 'r') as file:
        # use beautiful soup to parse the file
        soup = BeautifulSoup(file, 'html.parser')
        # find all the <p> tags
        paragraphs = soup.find_all('p')
        # for each <p> tag
        for paragraph in paragraphs:
            # get the quotes
            quotes = get_quotes(paragraph.text)

            paragraph.string = "NEW TEXT " + paragraph.text

            # what I need to do is find
            quotes_pattern = r'“[^”]*”'

            # Find all occurrences of the pattern
            quotes = re.findall(quotes_pattern, paragraph)

            # for each quote, determine if it needs a translation by calling a separate function
            # if it does, translate it
            # and then add a popup superscript number to the end of the quote
            # and then add a popup footnote to the end of the paragraph
            # if it doesn't, do nothing
            for quote in quotes:
                if needs_translation(quote):
                    # translate the quote
                    translation = translate(quote)
                    # add a popup superscript number to the end of the quote
                    # add a popup footnote to the end of the paragraph


            # modify the text of the <p> tag to put "NEW TEXT" in front of each quote
            #for quote in quotes:
            #    # replace the quote with "NEW TEXT" + the quote
            #    paragraph.text.replace(quote, "NEW TEXT " + quote)

        # write the modified chapter file to a new file
        with open('modified_chapter.html', 'w') as modified_file:
            modified_file.write(soup.prettify())

