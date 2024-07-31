from flask import Flask, request, render_template, jsonify, send_file
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from googletrans import Translator
from fpdf import FPDF
import os
import nltk
from nltk import word_tokenize, pos_tag

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

# Load the summarization model from the transformers library
summarizer = pipeline("summarization")
translator = Translator()

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def my_form_post():
    if request.method == 'POST':
        youtube_video = request.form['video_url']
        video_id = youtube_video.split("=")[1]

        try:
            # Get video transcript using youtube_transcript_api
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            # Combine transcript text into a single string
            transcript_text = ' '.join([entry['text'] for entry in transcript])

            # Generate a summary of the transcript using the summarization model
            num_iters = int(len(transcript_text) / 1000)
            summarized_text = []

            for i in range(0, num_iters + 1):
                start = i * 1000
                end = (i + 1) * 1000
                out = summarizer(transcript_text[start:end])
                out = out[0]
                out = out['summary_text']
                summarized_text.append(out)

            summarized_text = ' '.join(summarized_text)

            # Format the summarized text
            formatted_text = format_text(summarized_text)

            return render_template("index.html", transcription=formatted_text, video_url=youtube_video)

        except Exception as e:
            return jsonify({'error': 'Error fetching video transcript or generating a summary.'}), 500

def format_text(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    formatted_sentences = []

    for sentence in sentences:
        # Tokenize the sentence into words and tag parts of speech
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)

        # Capitalize nouns and the first word of the sentence
        formatted_words = []
        for i, (word, tag) in enumerate(tagged_words):
            if tag.startswith('NN') or i == 0:
                formatted_words.append(word.capitalize())
            else:
                formatted_words.append(word)

        formatted_sentence = ' '.join(formatted_words)
        formatted_sentences.append(formatted_sentence)

    return ' '.join(formatted_sentences)

@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    if request.method == 'POST':
        transcription = request.form['transcription']
        video_url = request.form['video_url']
        heading = "YouTube Video Summarization"

        pdf = FPDF()
        pdf.add_page()
        
        # Set font for heading (bold)
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt=heading, ln=True, align='C')
        
        # Set font for video URL (underline)
        pdf.set_font("Arial", style='U', size=12)
        pdf.cell(200, 10, txt=f"Video URL: {video_url}", ln=True, align='L')
        
        # Set font for transcription (normal)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=transcription, align='L')
        
        pdf_file_path = 'transcription.pdf'
        pdf.output(pdf_file_path)
        return send_file(pdf_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run()
