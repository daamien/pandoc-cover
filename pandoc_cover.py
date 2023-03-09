#!/usr/bin/env python3

"""
Generate de PDF cover using an SVG template and
the document metadata
"""

import subprocess
import tempfile

import jinja2 as jj2
import panflute as pf

FILTER_NAME="pandoc-cover"

def append_rawinline_in_metadata(doc, key, value, raw_format ='latex'):
    """
    Add content inside a pandoc metadata parameter
    """
    if key not in doc.metadata:
        doc.metadata[key] = pf.MetaList()
    doc.metadata[key].append(
        pf.MetaInlines(pf.RawInline(value, raw_format))
    )

def insert(doc,page,where):
    """
    Insert a page in the head of the document

    where: the pandoc metadata key where we append the raw latex code
    """
    if page not in [ 'front', 'inside-front', 'inside-back', 'back']:
        return

    if where not in ['include-before','include-after']:
        return

    svg_template=doc.get_metadata(FILTER_NAME+'.'+page)
    if svg_template is None:
        return

    # Open the SVG template
    env = jj2.Environment(loader=jj2.FileSystemLoader('.'))
    template = env.get_template(svg_template)

    # Render the SVG content
    svg_output = template.render(doc.get_metadata())

    # Save the results into an intermediary SVG file
    # In verbose mode, keep the file for debugging
    delete_svg=not doc.get_metadata('panflute-verbose',False)
    svg_file=tempfile.NamedTemporaryFile(mode='w',
                                             prefix=FILTER_NAME+'-',
                                             suffix=".svg",
                                             delete=delete_svg)
    svg_file.write(svg_output)
    svg_file.flush()

    # the PDF file can't be deleted because xelatex will use it later
    # in the pandoc generation proces
    pdf_file_path=svg_file.name+'.pdf'

    try:
        result=subprocess.run([ "rsvg-convert",
                                "--format=pdf",
                                "--output="+pdf_file_path,
                                svg_file.name],
                                check=True)
        if doc.get_metadata('panflute-verbose',False):
            pf.debug(FILTER_NAME+": "+' '.join(result.args))
    except FileNotFoundError:
        pf.debug(FILTER_NAME+": rsvg-convert is not found")
    except subprocess.CalledProcessError as err:
        pf.debug(FILTER_NAME+": rsvg-convert error")
        pf.debug(err)
    finally:
        svg_file.close()

    raw_latex = r'\includepdf{' + pdf_file_path + r'}'
    append_rawinline_in_metadata(doc,where,raw_latex)


def prepare(doc):
    """
    Generate the front page and inside-front page
    and insert them at the top of the document
    """
    if not FILTER_NAME in doc.metadata:
        return
    insert(doc,'front','include-before')
    insert(doc,'inside-front','include-before')


def action(elem, doc):
    """
    Nothing to do
    """
    return

def finalize(doc):
    """
    Insert back and inside-back pages
    and load the required latex settings
    """
    if not FILTER_NAME in doc.metadata:
        return

    raw_latex = r'\usepackage{pdfpages}'

    if doc.get_metadata(FILTER_NAME+'.disable_maketitle', True):
        raw_latex += r'\renewcommand\maketitle{}'

    append_rawinline_in_metadata(doc,'header-includes',raw_latex)

    insert(doc,'inside-back','include-after')
    insert(doc,'back','include-after')


def main(doc=None):
    """
    Define the filter actions
    """
    return pf.run_filter(action,
                         prepare=prepare,
                         finalize=finalize,
                         doc=doc)

if __name__ == '__main__':
    main()
