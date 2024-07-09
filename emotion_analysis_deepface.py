from deepface import DeepFace
import cv2
import numpy as np

def analyze_emotion_deepface(file):
  # 파일을 읽어서 OpenCV 이미지로 변환
  file_bytes = np.frombuffer(file.read(), np.uint8)
  image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

  try:
    # DeepFace를 사용하여 표정 인식 (얼굴이 감지되지 않았을 때 error가 나지 않게 하는 방법: enforce_detection=False 추가)
    results = DeepFace.analyze(image, actions=['emotion'])
    return results[0]['emotion']
  except ValueError as e:
    # 얼굴이 감지되지 않았을 때 예외 처리
    return {'error': str(e)}

