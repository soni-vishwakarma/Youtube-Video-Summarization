# Youtube_Video_Summarization
I developed this YouTube Video Summarizer using Python, HTML, and JavaScript. It uses a Python Flask API to fetch transcripts from YouTube videos, generate a summarized version using a transformer-based model, and format the text with proper capitalization using the NLTK (Natural Language Toolkit) library. It also displays the video and allows users to download the summary as a PDF.

**Install all the necessary libraries before running the code**

**Usage**
1. Run the Flask application: python app.py
2. Open your web browser and go to http://127.0.0.1:5000/. Enter the YouTube video URL and click “Transcribe”.
   ![Screenshot 2024-07-30 222117](https://github.com/user-attachments/assets/feb0ea2e-46b9-4b18-aaf0-f33199ddaf57)

3. The video will be displayed immediately, and the summarization process will start. A rotating spinner will indicate the progress.
   ![Screenshot 2024-07-30 221530](https://github.com/user-attachments/assets/22d3f77e-4179-4bd9-8a79-a8811df846f5)

4. Once the summarization is complete, the summary will be displayed. You can download the summary as a PDF by clicking the “Download PDF” button.
   ![Screenshot 2024-07-30 221927](https://github.com/user-attachments/assets/594437e7-3481-453f-9439-035c6196c2ad)

