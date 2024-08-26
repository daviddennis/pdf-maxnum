# Coding Assignment Submission for Conductor AI

Finds the maximum number in a given PDF file

## Usage

```sh
    pip install -r requirements.txt
    python main.py <PDF_FILENAME>
```
OR
```sh
    python main.py 
```
Note: As a small added feature, if the PDF filename is not provided as an argument,
the script will look for and use the first PDF file it finds in the current directory

## Details

- *python 3.6+*
- Uses `pymupdf` to extract PDF text & pages
- Uses a variable context window length to predict the intended values of numbers (e.g., "in millions)", "256K")

(Expected Output: 35,110,000,000)