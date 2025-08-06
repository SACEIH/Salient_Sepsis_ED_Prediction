# Salient: Sepsis ED Prediction


pandoc 00_00_Cover_Text.md 01_00_Cohort.md  08_00_Journey.md 08_01_icd-10.md 90_01_ed_sql.md 99_00_References.md  --filter pandoc-crossref --citeproc -o example.pdf --from markdown --template eisvogel --listings --variable papersize=a4  --number-sections 

pandoc 00_00_Cover_Text.md 01_00_Cohort.md  08_00_Journey.md 08_01_icd-10.md 90_01_ed_sql.md 99_00_References.md  --filter pandoc-crossref --citeproc -o example.tex --from markdown --listings --template eisvogel --variable papersize=a4  --number-sections 

pandoc ./00_00_Cover_Text.md  .\90_01_ed_sql.md -o test.tex --listings --template eisvogel --number-sections   --variable papersize=a4   --standalone

pandoc --template eisvogel --filter pandoc-crossref  --listings --number-sections  --citeproc --variable papersize=a4   --standalone  ./00_00_Cover_Text.md  .\90_01_ed_sql.md -o test.tex 


pandoc --template eisvogel --filter pandoc-crossref  --listings --number-sections  --citeproc --variable papersize=a4   --standalone  00_00_Cover_Text.md 01_00_Cohort.md  02_00_Demographics.md 08_00_Journey.md 08_01_icd-10.md  08_02_Cohort_ICD10.md  90_01_ed_sql.md 99_00_References.md -o test.tex 