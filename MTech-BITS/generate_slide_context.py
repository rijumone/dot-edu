import PyPDF2
import click
import requests
import json

url = "http://192.168.1.16:11434/api/generate"


headers = {
  'Content-Type': 'application/json'
}

@click.command()
@click.argument('pdf_file', type=click.Path(exists=True))
def pdf_to_text(pdf_file):
    """Converts a PDF file to text."""
    # Create a PdfReader object from the file
    pdf_reader = PyPDF2.PdfReader(open(pdf_file, 'rb'))

    # Get the number of pages in the PDF
    # num_pages = pdf_reader.numPages
    page_num = 0
    for page_obj in pdf_reader.pages:
        # page_obj = pdf_reader.getPage(page_num)
        text = page_obj.extract_text()
        
        if text:  # If there is text on the page, print it
            # print(f":")
            # print(text)
            pre_prompt = 'Name the topic being discussed in the following text in 10 words or less.\n'
            payload = json.dumps({
                # "model": "llama3.1:latest",
                "model": "gemma2:latest",
                "prompt": f"{pre_prompt} {text}",
                "stream": False
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            print(f"Page {page_num+1}: {json.loads(response.text).get('response').rstrip('\n')}")

        page_num += 1

# Call the function with the PDF file name as argument
# pdf_to_text('/Users/rijumone/Downloads/WILP/Sem2/DRL/Slides/DRL-all-except-last-slides-merged.pdf')
if __name__ == '__main__':
    pdf_to_text() 