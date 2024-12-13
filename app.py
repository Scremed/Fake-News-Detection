from flask import Flask, render_template, request, url_for
import torch
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification

app = Flask(__name__)

# Load the fine-tuned model
def load_model(model_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = BertForSequenceClassification.from_pretrained("indobenchmark/indobert-base-p2")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

# Tokenize the input text
def tokenize_text(text, tokenizer):
    return tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")

# Make predictions
def predict(model, tokenizer, text):
    tokens = tokenize_text(text, tokenizer)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokens = {key: val.to(device) for key, val in tokens.items()}
    with torch.no_grad():
        outputs = model(**tokens)
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1).cpu().numpy()
    pred_label = np.argmax(probs, axis=1)
    return pred_label, probs

# Example usage
model_path = "model\indobertModel.pt"
model = load_model(model_path)
tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-base-p2")

# Label mapping
label_map = {0: "Fakta", 1: "Hoax"}

@app.route('/')
def index():
    return render_template('index.html', news_text=None, predicted_label=None, predicted_prob=None)

@app.route('/check', methods=['POST'])
def check():
    news_text = request.form['news_text']
    pred_label, probs = predict(model, tokenizer, news_text)
    predicted_label = label_map[pred_label[0]]
    predicted_prob = probs[0][pred_label[0]]
    return render_template('index.html', 
                           news_text=news_text, 
                           predicted_label=predicted_label, 
                           predicted_prob=predicted_prob)

if __name__ == '__main__':
    app.run(debug=True)
