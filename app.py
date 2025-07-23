from flask import Flask, request, render_template
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk
import cv2
import pytesseract
from PIL import Image
import io
import numpy as np
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
# Ensure NLTK punkt is downloaded
nltk.download('punkt')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    choice = request.form.get('choice')
    data = ""

    if choice == '1':  # Textual Input
        user_input = request.form.get('text_input')
        data = user_input
    elif choice == '2':  # Image Input
        file = request.files['image_input']
        img = Image.open(file.stream)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        data = pytesseract.image_to_string(img_cv, lang='eng', config='--psm 1')
    
    # Initialize the parser and summarizer
    parser = PlaintextParser.from_string(data, Tokenizer('english'))
    lex_rank_summarizer = LexRankSummarizer()
    summary = lex_rank_summarizer(parser.document, sentences_count=5)
    
    # Convert summary sentences into a single string
    summary_text = "\n".join(str(sentence) for sentence in summary)
    
    # Render template with summary and input data
    return render_template('summary.html', summary=summary_text, input_data=data)

if __name__ == '__main__':
    app.run()
