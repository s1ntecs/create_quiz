import asyncio
from fastapi import APIRouter, Depends
from database.connection import get_session
from models.quiz import Question, QuestionsCount
from services.services import add_questions_to_db
from sqlalchemy import desc

quiz_router = APIRouter(
    tags=["Quiz"],
)


@quiz_router.post("/new")
async def create_question(count: QuestionsCount,
                          session=Depends(get_session)
                          ) -> dict:
    last_question = (session.query(Question)
                     .order_by(desc(Question.id)).first())
    question = last_question.to_dict() if last_question else None
    asyncio.create_task(add_questions_to_db(count.questions_num, session))
    return question
