# Web scrap TED talk links

## Overview 
This project performs web scraping to extract content from a specific webpage. It uses the <code>requests</code> library to fetch the HTML content of the page and the <code>BeautifulSoup</code> library to parse the HTML and extract text from a designated section of the page. 

## Key Features 
- Fetches HTML Content: The script sends a GET request to the specified URL (https://gongjyuhok.hk/articles/10671) to retrieve the webpage's HTML.
- Parses HTML: It uses BeautifulSoup to parse the HTML content.
- Extracts Text: The script looks for a <div> element with the class entry-content and retrieves the text within that div, printing it to the console.
- Error Handling: If the specified div is not found, it prints a message indicating that the content div was not found.

## Use Case
This script is useful for anyone looking to scrape specific content from a webpage, particularly for extracting text from structured HTML elements.

## Using the Code
1. Install Required Libraries: Ensure you have the required libraries installed. You can install them using pip: pip install requests beautifulsoup4
2. Run the Script: Save the code in a Python file. Run the script using Python: python filename.py
3. View Output: The script will print the extracted text from the specified div to the console. If the div is not found, it will print "Content div not found."

## Requirements to Run the Code
Python: Ensure you have Python installed on your machine (Python 3.x is recommended).
Libraries: The following libraries must be installed:
requests: For making HTTP requests to fetch the webpage.
beautifulsoup4: For parsing the HTML content.


   
