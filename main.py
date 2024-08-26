#!/usr/bin/env python3
import sys, pymupdf

CONTEXT_WINDOW_SIZE = 1500

def adjust_number_per_text_context(number: float|int, text_context_before: str, text_context_after: str):
    """
    Adjusts the number based on the text context before and after it.
    """

    if 'in thousands)' in text_context_before:
        number *= 1000
    elif 'in millions)' in text_context_before:
        number *= 1000000
    elif 'in billions)' in text_context_before:
        number *= 1000000000
    elif 'in trillions)' in text_context_before:
        number *= 1000000000000
    else:
        if text_context_after.startswith(' thousand') or text_context_after.startswith('k '):
            number *= 1000
        elif text_context_after.startswith(' million') or text_context_after.startswith('m '):
            number *= 1000000
        elif text_context_after.startswith(' billion') or text_context_after.startswith('b '):
            number *= 1000000000
        elif text_context_after.startswith(' trillion') or text_context_after.startswith('t '):
            number *= 1000000000000

    return number

def get_max_number_from_text(pages: list[str]) -> float|int|None:
    """
    Extracts numbers from the text of the PDF pages and returns the maximum number found.
    We construct numbers one character at a time - starting from the first digit encountered.
    When a non-digit character is encountered, we check if the number is considered valid, and make adjustments.
    """
    max_num = None

    number_str = ''
    in_number = False
    end_of_number = False

    for page_text in pages:
        for char_pos, c in enumerate(page_text):
            if c.isdigit():
                if not in_number:
                    in_number = True
                number_str += c
            elif c == ',':
                pass
            elif c == '.':
                if in_number:
                    if '.' in number_str:
                        # Avoid multiple decimal points
                        end_of_number = True
                    else:
                        number_str += c
            else:
                end_of_number = True
            
            if end_of_number:
                end_of_number = False

                if in_number:
                    in_number = False

                    try:
                        found_number = float(number_str) if '.' in number_str else int(number_str)
                    except ValueError:
                        number_str = ''
                        continue

                    text_context_before = page_text[max(0, char_pos-CONTEXT_WINDOW_SIZE):char_pos].lower()
                    text_context_after = page_text[char_pos:char_pos+CONTEXT_WINDOW_SIZE].lower()

                    found_number = adjust_number_per_text_context(found_number, text_context_before, text_context_after)

                    if max_num is None or found_number > max_num:
                        max_num = found_number

                    number_str = ''

    return max_num

def main():
    # Open PDF file
    try:
        if len(sys.argv) >= 2:
            pdf_file = pymupdf.open(sys.argv[1])
        else:
            raise pymupdf.FileNotFoundError
    except pymupdf.FileNotFoundError:
        # If no filename provided, find the first pdf in the current directory, and use that
        import glob
        pdf_files = sorted(glob.glob('*.pdf') + glob.glob('*.PDF'))
        if pdf_files:
            pdf_filename = pdf_files[0]
            try:
                pdf_file = pymupdf.open(pdf_filename)
            except pymupdf.FileNotFoundError:
                print(f'Error: File "{pdf_filename}" could not be opened.')
                exit(1)
        else:
            print('Error: No PDF files found in the current directory.')
            exit(1)

    # Extract text from pages
    pdf_pages = [page.get_text() for page in pdf_file]

    # Find maximum number
    max_num = get_max_number_from_text(pdf_pages)

    if max_num is None:
        print('No numbers found in the PDF.')
        exit(1)

    # Print maximum number
    if max_num == int(max_num):
        print(f'{int(max_num):,}')
    else:
        print(f'{max_num:.2f}')

if __name__ == '__main__':
    main()