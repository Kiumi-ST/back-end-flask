from flask import Flask, request, jsonify
from model import db
import os
from google.cloud import secretmanager

# 환경 변수 설정 (oneDNN 옵션 비활성화)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# TensorFlow 로그 수준 설정
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

# emotion_analysis_deepface.py 파일에서 analyze_emotion 함수 임포트
from emotion_analysis_deepface import analyze_emotion_deepface

app = Flask(__name__)

# MySQL 데이터베이스 URI 설정
# Secret Manager에서 비밀을 가져오는 함수
def get_secret(project_id, secret_id):
  client = secretmanager.SecretManagerServiceClient()
  secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/1"
  response = client.access_secret_version(name=secret_name)
  secret_value = response.payload.data.decode("UTF-8")
  return secret_value

# Secret Manager에서 비밀 값을 가져와 환경 변수로 설정
project_id = "390459592108"
secret_id = "DATABASE_URI"
os.environ['DATABASE_URI'] = get_secret(project_id, secret_id)

# Flask 앱 설정에 환경 변수를 사용
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not app.config['SQLALCHEMY_DATABASE_URI']:
  raise RuntimeError("The DATABASE_URI environment variable is not set.")

# SQLAlchemy와 앱을 연동
db.init_app(app)

# 테이블 초기화, 테이블 생성
# with app.app_context():
#   db.create_all()
  
@app.route('/analyze-deepface', methods=['POST'])
def analyze_deepface():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'}), 400

  file = request.files['file']
  screen_name = request.form.get('screen_name')

  if not file.filename:
    return jsonify({'error': 'No selected file'}), 400
  if not screen_name:
    return jsonify({'error': 'No screen name provided'}), 400

  # 파일과 화면 이름을 분석 함수로 전달
  result = analyze_emotion_deepface(file, screen_name)
  if 'error' in result:
    return jsonify(result), 500
  return jsonify(result)

@app.route('/') # 서버 테스트
def home():
  return "Hello, Flask!"

if __name__ == '__main__':
  app.run(port=8000, host='0.0.0.0')