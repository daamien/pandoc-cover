#!/usr/bin/env python3

"""
Generate de PDF cover using an SVG template and
the document metadata
"""

import os
import subprocess

import jinja2 as jj2
import panflute as pf

##
## This is a parameter defined by the eisvogel template
## https://github.com/Wandmalfarbe/pandoc-latex-template#custom-template-variables
##
TAG="titlepage-background"


def prepare(doc):
    """
    Generate a PDF and use as the cover of the document
    """
    if TAG in doc.metadata:
        # Open the SVG template
        template_file=pf.stringify(doc.metadata[TAG])
        file_loader = jj2.FileSystemLoader('.')
        env = jj2.Environment(loader=file_loader)
        template = env.get_template(template_file)
        # The metadata is stored inside pf.MetaInlines objects
        meta = {}
        for k in doc.metadata.content:
            meta[k]= pf.stringify(doc.metadata[k])
        # Render the SVG content
        svg_output = template.render(meta)
        # Save the results into a temporary SVG file
        path, name = os.path.split(template_file)
        svg_file=os.path.join(path,'_'+name)
        with open(svg_file, "w", encoding="utf-8") as file_handler:
            file_handler.write(svg_output)
        # Convert the SVG File into a temporary PDF file
        pdf_file=svg_file+".pdf"
        try:
            subprocess.run(["rsvg-convert",
                            "--format=pdf",
                            "--output="+pdf_file,
                            svg_file],
                            check=True)
        except FileNotFoundError:
            print("pandoc-conver: rsvg-convert is not found")
            # handle file not found error.

        # Change the metadata
        # /!\ this is not useful at the moment
        doc.metadata[TAG]=pdf_file
        # Insert the PDF page at the beginning of the document
        if "header-includes" not in doc.metadata:
            doc.metadata["header-includes"] = pf.MetaList()
        doc.metadata["header-includes"].append(
            pf.MetaInlines(pf.RawInline("\\usepackage{pdfpages}", "tex"))
        )
        code =r'\includepdf{'+pdf_file+r'}'
        code+=r'\pagebreak'
        doc.content.insert(0,pf.RawBlock(code,format='latex'))

def action(elem, doc):
    """
    Nothing to do
    """
    return

def main(doc=None):
    """
    Define the filter actions
    """
    return pf.run_filter(action,
                         prepare=prepare,
                         doc=doc)

if __name__ == '__main__':
    main()
