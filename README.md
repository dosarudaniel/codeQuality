# A Code Analysis Tool to Help Students in the Age of Generative AI :
This repository contains the SimplePMD application used in paper [A Code Analysis Tool to Help Students in the Age of Generative AI](https://link.springer.com/chapter/10.1007/978-3-031-72312-4_31)

## Types of workflows
### For students (individual use)
#### How to run the web version and assess your code quality OOP metrics :
1. `git clone`
2. `cd codeQuality`
3. `python app.py`
4. open this webpage [127.0.0.1:5000](http://127.0.0.1:5000/)

### For teachers (batch processing)
#### How to run the .jar file quality tool:
- Step1. Install java for Windows / Linux / macOS from: [Oracle](https://www.oracle.com/java/technologies/downloads/)
- Step2. Place the code into resources/input/responses.csv column E, add a student name (e.g. student1), challenge name and score if available otherwise `N\A`
- Step 2.1 Delete all the files from PmdSimple_main_jar\resources\input\entries
- Step3. Run this command:
   `java -jar PmdSimple-main.jar`
- Step4. Analize the results from `resources/output/output.csv` file.

## [Run time performance data](https://docs.google.com/spreadsheets/d/1J8VJJHX5ddk0zJ6Njvb5nMmNfLzSTKEWHw-ZJg4dzcA/edit?usp=sharing)
For batch processing the SimplePMD tools can analyzes hundreds of coding assignments in a few seconds

![SimplePMD runtime](https://github.com/user-attachments/assets/3d77986a-f6a2-455c-b9c3-9fed5d6dfac0)    
Each file has approximately 126 lines of java code
