# Text-Analysis

Instructions Documentation

Project Overview
This project focuses on extracting and analyzing article content from URLs provided in an Excel file. The goal is to conduct sentiment and readability analysis on the extracted text, generating various textual metrics. The final results will be saved in a CSV or Excel file for further review.
Approach to the Solution
1.	Data Extraction:
•	Libraries Used:
	pandas for handling Excel files.
	requests for retrieving webpage content.
	BeautifulSoup from bs4 for parsing HTML and extracting article content.
•	Process:
	Read the input Excel file (e.g., Input.xlsx) using pandas.
	For each URL in the file, retrieve the webpage content using the requests library.
	Use BeautifulSoup to parse the HTML content and extract the article's main text, while avoiding non-essential elements like headers, footers, and ads.
	Save the extracted text in a .txt file, named based on the URL_ID.
2.	Textual Analysis:
•	Libraries Used:
	nltk for natural language processing tasks like stop word removal and tokenization.
	re for regular expression-based calculations, such as counting personal pronouns.
•	Process:
	Sentiment Analysis:
o	Clean the text by removing stop words.
o	Calculate the Positive Score, Negative Score, Polarity Score, and Subjectivity Score using predefined dictionaries.
	Readability Analysis:
o	Compute the Fog Index based on average sentence length and the percentage of complex words.
	Other Metrics:
o	Measure word count, syllable count per word, complex word count, average word length, and other specified variables.
3.	Output Structure:
•	Save the results in an Excel file named Output Data Structure.xlsx, adhering to the structure provided in the project guidelines.
How to Run the .py File
1.	Install Dependencies:
•	Make sure you have Python installed (version 3.7 or higher is recommended).
•	Install the necessary Python libraries using pip:
•	pip install pandas requests beautifulsoup4 nltk openpyxl
•	Alternatively, you can install all dependencies from a requirements.txt file:
•	pip install -r requirements.txt
2.	Running the Script:
•	Ensure that Input.xlsx, the StopWords folder, and the MasterDictionary folder are in the same directory as the Python script.
•	Run the script with the following command:
•	python text_analysis.py
•	The script will read URLs from Input.xlsx, extract the corresponding article text, perform the required analysis, and save the results in Output Data Structure.xlsx.
3.	Expected Outputs:
•	The extracted text files will be saved with filenames corresponding to their URL_ID (e.g., 101.txt).
•	The analysis results will be saved in Output Data Structure.xlsx, ready to be opened in Excel or any other spreadsheet software.
Dependencies
•	Python: Version 3.7 or higher
•	Libraries: pandas, requests, beautifulsoup4, nltk, openpyxl
•	Additional Resources: StopWords folder, MasterDictionary folder
Additional Notes
•	Ensure that the script and all required files are in the same directory to avoid file path issues.
•	If you encounter encoding errors during text extraction, the script saves text files in UTF-8 encoding to handle them.
