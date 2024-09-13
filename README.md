# codeQuality
This repo contains the tools used for paper A Code Analysis Tool to Help Students in the Age of Generative AI

[Paper link](https://link.springer.com/chapter/10.1007/978-3-031-72312-4_31)


How to run Code quality tool:

Step1. Install java for Windows / Linux / macOS from: [Oracle](https://www.oracle.com/java/technologies/downloads/)

Step2. Place the code into PmdSimple_main_jar\resources\input\responses.csv column E, add a student name (e.g. student1), problem name and score if available otherwise N\A

Step 2.1 Delete all the files from PmdSimple_main_jar\resources\input\entries

Step3. Run this command:

   java -jar PmdSimple-main.jar

Step4. Analize the results from PmdSimple_main_jar\resources\output\my_students.csv file.


