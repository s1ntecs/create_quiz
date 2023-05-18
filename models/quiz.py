from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()

class QuestionsCount(BaseModel):
    questions_num: int

    class Config:
        schema_extra = {
            "example": {
                "questions_num": 3
            }
        }

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, index=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "question": self.question,
            "answer": self.answer,
            "created_at": self.created_at.isoformat(),
        }
