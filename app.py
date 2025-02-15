import os
from flask import Flask, render_template, request, jsonify, flash, session
from summarizer import summarize_text
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this in production

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data.get('text', '')
        summary_length = data.get('summary_length', 'medium')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Check if text exceeds limit (10,000 chars for demo purposes)
        if len(text) > 10000:
            return jsonify({'error': 'Text exceeds 10,000 character limit'}), 400
        
        # Call the summarization function
        summary = summarize_text(text, summary_length)
        
        return jsonify({'summary': summary})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)