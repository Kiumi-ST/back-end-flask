from deepface import DeepFace
import cv2
import numpy as np
from model import db, UserDifficultyPage

def analyze_emotion_deepface(file, screen_name):
  # 파일을 읽어서 OpenCV 이미지로 변환
  file_bytes = np.frombuffer(file.read(), np.uint8)
  image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

  # 이미지 크기 축소
  image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)

  try:
    # DeepFace를 사용하여 표정 인식 
    # (얼굴이 감지되지 않았을 때 error가 나지 않게 하는 방법: enforce_detection=False 추가)
    results = DeepFace.analyze(image, actions=['emotion'])
    emotions = results[0]['emotion']

    # 가장 우세한 감정을 검색
    dominant_emotion = max(emotions, key=emotions.get)

    # 우세한 감정이 'happy', 'neutral' 중 하나라면 사용자가 어려움을 겪고 있지 않다고 판단
    if dominant_emotion in ['happy', 'neutral']:
      is_difficult = False   
    else:
      # 부정적인 감정 상태 목록
      difficult_emotions = ['angry', 'disgust', 'fear', 'sad', 'surprise']
      # 감정 상태 중 하나라도 부정적이라면 isDifficult를 True로 설정(임계값: 0.5)
      is_difficult = any(emotions[emotion] > 0.5 for emotion in difficult_emotions)

      # 감정이 부정적이라고 판단된 경우 DB에 화면 이름과 감정 상태를 저장
      if is_difficult:
        new_entry = UserDifficultyPage(screen_name=screen_name, emotion=dominant_emotion)
        db.session.add(new_entry)
        db.session.commit()

    return {"isDifficult": is_difficult, "dominantEmotion": dominant_emotion}
  
  except ValueError as e:
    # 얼굴이 감지되지 않았을 때의 예외 처리
    return {'error': 'No face detected.'}
  
  except Exception as e:
    # 기타 예외 처리
    return {'error': f'An error occurred: {str(e)}'}

