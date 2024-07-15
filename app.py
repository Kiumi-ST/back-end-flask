from flask import Flask, request, jsonify
import os

# 환경 변수 설정 (oneDNN 옵션 비활성화)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# TensorFlow 로그 수준 설정
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

# emotion_analysis_deepface.py 파일에서 analyze_emotion 함수 임포트
from emotion_analysis_deepface import analyze_emotion_deepface

app = Flask(__name__)
  
@app.route('/analyze-deepface', methods=['POST'])
def analyze_deepface():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'}), 400

  file = request.files['file']
  if file.filename == '':
    return jsonify({'error': 'No selected file'}), 400

  if file:
    # 파일을 읽어서 OpenCV 이미지로 변환
    result = analyze_emotion_deepface(file)
    if 'error' in result:
      return jsonify(result), 500
    return jsonify(result)

@app.route('/') # 서버 테스트
def home():
  return "Hello, Flask!"

if __name__ == '__main__':
  app.run(port=8080)