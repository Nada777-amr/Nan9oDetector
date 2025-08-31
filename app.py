from flask import Flask, request, jsonify
import joblib
from urllib.parse import urlparse
from tld import get_tld
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model once when the server starts
model = joblib.load("url_model_new.pkl")

def extract_features(url):
    hostname_length = len(urlparse(url).netloc)
    count_dir = urlparse(url).path.count('/')
    count_www = url.count('www')
    url_length = len(str(url))
    try:
        fd_length = len(urlparse(url).path.split('/')[1])
    except:
        fd_length = 0
    count_dash = url.count('-')
    count_dot = url.count('.')
    try:
        tld_length = len(get_tld(url, fail_silently=True))
    except:
        tld_length = -1
    count_digits = sum(c.isdigit() for c in url)
    count_equal = url.count('=')
    
    return {
        'hostname_length': hostname_length,
        'count_dir': count_dir,
        'count-www': count_www,
        'url_length': url_length,
        'fd_length': fd_length,
        'count-': count_dash,
        'count.': count_dot,
        'tld_length': tld_length,
        'count-digits': count_digits,
        'count=': count_equal
    }

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    features = extract_features(url)
    
    # Model expects features in the same order as training
    feature_order = [
        'hostname_length', 'count_dir', 'count-www',
        'url_length', 'fd_length', 'count-', 'count.',
        'tld_length', 'count-digits', 'count='
    ]
    
    feature_vector = [features[feat] for feat in feature_order]
    prediction = model.predict([feature_vector])[0]
    label_map = {0: "Benign", 1: "Malicious"}
    
    return jsonify({
        'url': url,
        'prediction': label_map[prediction]
    })

@app.route('/check_url', methods=['POST'])
def check_url():
    data = request.get_json(force=True)
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    features = extract_features(url)
    feature_order = [
        'hostname_length', 'count_dir', 'count-www',
        'url_length', 'fd_length', 'count-', 'count.',
        'tld_length', 'count-digits', 'count='
    ]
    feature_vector = [features[feat] for feat in feature_order]
    prediction = model.predict([feature_vector])[0]
    
    # safe = True if benign (0), False if malicious (1)
    safe = (prediction == 0)
    
    return jsonify({'safe': safe})

if __name__ == '__main__':
    app.run(debug=True)
