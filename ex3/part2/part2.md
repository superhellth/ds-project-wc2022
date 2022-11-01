# Solutions for part two of exercise 3 of assignment 1
by Raphael Ebner, Nicolas Hellthaler, Bastian Müller

## Why is a high quality conversion from PDF to plaintext hard?
There are many specific reasons why the conversion is hard.
Mainly it has to do with the heterogeneity of PDF files. In this exercise alone we've seen many kinds of examples.
Because PDFs in general don't follow the same formatting, finding a 'one-size-fits-all' solution is almost impossible.
Given the flexibility of the PDF format, text is not stored as words, sentences or paragraphs.
PDFs internally contain only characters and rules on where to draw them. So accessing the text afterwards is not straightforward.

The following article provides some more concrete examples (https://filingdb.com/b/pdf-text-extraction):

- Off-page characters
  - will show up when extracting text even though they are not visible when looking at the PDF file because they are for example hidden behind an image
- Small or invisible characters
  - can make it hard to access desired text because there is for example white text on a white page behind some black text
- Too little or too many spaces
  - make it hard to make out what a word is. For example in our extraction with 'pdfminer' of the 'flyers/bahnstadt.pdf' document we got 'BERGH EIM' instead of 'BERGHEIM'
