# Alternative Document Creation 

The proposed document is based on markdown which is a simple text based system
that has the benefit of separating writing from type setting. It uses latex and
pandoc to create the finished product. 

## Software 

- Latex: https://miktex.org/download  
    I recommend installing Miktex with a full installation. Go to the all download and use the Net installer to get a full installation. https://miktex.org/download. This reduces problems with missing packages later on. 
- Pandoc: https://pandoc.org/  
    This is a document conversion system which is used to build the document. 
    


## Setup 

After installing pandoc and Miktex you need to install the template for the document and a plugin for citations. 

Drive E: is  CI-DATA 

Copy the file E:\Pandoc - Examples\eisvogel.latex to the directory
C:\Users\ibertr02\AppData\Roaming\pandoc\templates replacing ibertr02 with your
user name. 

Copy the file E:\Pandoc - Examples\pandoc-crossref.exe to the pandoc executable
directory which is  C:\Program Files\Pandoc\ on my system. 

If you have problems you my need to add pandoc to the path on your computer. 

## Example script 

Copy the directory E:\Pandoc - Examples\Report_Markdown to a location of your
own and cd  to that directory. In that directory run the following command 

```
pandoc --template eisvogel --filter pandoc-crossref  --listings --number-sections  --citeproc --variable papersize=a4   --standalone  00_00_Cover_Text.md 01_00_Cohort.md  02_00_Demographics.md 08_00_Journey.md 08_01_icd-10.md  08_02_Cohort_ICD10.md  90_01_ed_sql.md 99_00_References.md -o test.pdf
```

To edit the title and other information look in the first markdown file
00_00_Cover_Text.md. The top text block sets the metadata for the document (which includes the front page and other graphics needed for the official headers and footers):

Examples of table citations are in the document. 

```markdown
---
title: "SALIENT: ED Machine Learning Sepsis Prediction"
author: "Iain A Bertram,"
date: "11 July 2025"
bibliography: report.bib 
csl: cell-numeric.csl    
toc-own-page: true
titlepage: true
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "360049"
titlepage-rule-height: 0
titlepage-background: "Word_document_template_back.png"
header-left: "\\hspace{1cm}"
header-center: "OFFICIAL: Sensitive"
header-right: "Page \\thepage"
footer-right: "\\hspace{1cm}"
footer-left: "\\hspace{1cm}"
footer-center: "Version 0.1"
geometry: "left=1cm,right=1cm,top=2.6cm,bottom=3.25cm"
page-background: "headers.pdf"
page-background-opacity: 0.5
code-block-font-size: "\\scriptsize"
listings: True
---
```

Citations are handled using the bibtex format as that is what I am familiar
with. The file report.bib has some examples. Most academic papers will have
citation information in bibtex format. If you only have endnote format (.ris)
you can use https://www.bruot.org/ris2bib/ to convert it or try to use the DOI
to get an entry https://www.bibtex.com/c/doi-to-bibtex-converter/.  

I use a physics (STEM) citation method which orders the references in the order
the appear in the document and labels them with numbers in square braces. e.g.
[1].  

Mathematical equations are formatted using latex: e.g. $\sin^2 x + \cos^2 x =
1$. It is mostly straight forward . You can find online editors to help.
https://latexeditor.lagrida.com/ 

Note: Both R and pandas in python allow you to export tables in markdown. 


## Useful Links

- Markdown table generator: https://www.tablesgenerator.com/markdown_tables for converting Excel tables into markdown. 

- latex equations: https://latexeditor.lagrida.com/


