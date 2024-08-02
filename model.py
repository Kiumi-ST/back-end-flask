from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 인스턴스 생성
db = SQLAlchemy()

# Flask에서 사용할 테이블 정의
class UserDifficultyPage(db.Model):
  __tablename__ = 'user_difficulty_page'
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  screen_name = db.Column(db.String(300), nullable=False)
  emotion = db.Column(db.String(255), nullable=False)

  def __init__(self, screen_name, emotion):
    self.screen_name = screen_name
    self.emotion = emotion
