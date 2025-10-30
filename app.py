from flask import Flask, render_template, request, jsonify
from utils.gesture_utils import recognize_gesture
from utils.translator import translate_text
from utils.voice_generator import generate_voice
import subprocess

# ✅ Create Flask app
app = Flask(__name__)

# ✅ Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Simulated gesture route
@app.route('/process_gesture', methods=['POST'])
def process_gesture():
    gesture = request.json.get('gesture')
    english_text = recognize_gesture(gesture)
    translated_text = translate_text(english_text, target_lang='kn')  # Kannada
    audio_path = generate_voice(translated_text)
    return jsonify({
        'english': english_text,
        'translated': translated_text,
        'audio': audio_path
    })

# ✅ Live gesture detection route
@app.route('/detect_gesture', methods=['POST'])
def detect_gesture():
    try:
        subprocess.run(['python', 'utils/gesture_recognition.py'], timeout=10)
        with open('gesture_output.txt', 'r') as f:
            gesture = f.read().strip()
        english_text = recognize_gesture(gesture)
        translated_text = translate_text(english_text, target_lang='kn')
        audio_path = generate_voice(translated_text)
        return jsonify({
            'gesture': gesture,
            'english': english_text,
            'translated': translated_text,
            'audio': audio_path
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# ✅ Start Flask server
if __name__ == '__main__':
    app.run(debug=True)