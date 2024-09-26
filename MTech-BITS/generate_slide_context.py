import PyPDF2
import click
import requests
import json

url = "http://192.168.1.16:11434/api/generate"

ALL_SUBJECT_TOKENS = {
    'DRL': """Here is the formatted version in Markdown:
# 1. Introduction: Introducing RL
# 2. MDP: Framework
# 3. Approaches to Solving Reinforcement Problems
# 4. Discussion on the Classification of (Deep) Reinforcement Learning Approaches, Algorithms, and Applications
# 5. Value-Based DRL Methods
# 6. Policy Gradients Methods
# 7. Model-Based Deep RL
# 8. Imitation Learning
# 9. Multi-Agent RL
# 10. (Optional Content) Special Topics
# 11. Course Summary
"""
}


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
            # pre_prompt = f'Name the topic being discussed in the following text in 10 words or less. Also from assign one single category to the topic among these.: \n{ALL_SUBJECT_TOKENS["DRL"]}\n . Output in one single line.\n'
            pre_prompt = f'Name the topic being discussed in the following text in 10 words or less. Just output the topic text, don\'t format it or say any additional text.\n'
            payload = json.dumps({
                # "model": "llama3.1:latest",
                "model": "gemma2:latest",
                "prompt": f"{pre_prompt} {text}",
                "stream": False
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            try:
                cleaned_response = json.loads(response.text).get('response').rstrip('\n')
            except AttributeError:
                cleaned_response = 'Unable to generate output'
            print(f"Slide {page_num+1}: {cleaned_response}")

        page_num += 1

# Call the function with the PDF file name as argument
# pdf_to_text('/Users/rijumone/Downloads/WILP/Sem2/DRL/Slides/DRL-all-except-last-slides-merged.pdf')
if __name__ == '__main__':
    pdf_to_text() 