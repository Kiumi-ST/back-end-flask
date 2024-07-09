from flask import Flask, request, jsonify

# emotion_analysis_deepface.py 파일에서 analyze_emotion 함수 임포트
from emotion_analysis_deepface import analyze_emotion_deepface

app = Flask(__name__)
  
@app.route('/analyze-deepface', methods=['POST'])
def analyze_deepface():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'})

  file = request.files['file']
  if file.filename == '':
    return jsonify({'error': 'No selected file'})

  if file:
    # 파일을 읽어서 OpenCV 이미지로 변환
    emotions = analyze_emotion_deepface(file)

    return jsonify({'emotions': emotions})

@app.route('/') # 서버 테스트
def home():
  return "Hello, Flask!"

if __name__ == '__main__':
  app.run(port=8080)