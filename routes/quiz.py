import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
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
    """ Функция создания вопросов и отправки
    в ответ одного последнего добавленного в БД вопроса. """
    try:
        last_question = (session.query(Question)
                         .order_by(desc(Question.id)).first())
        question = last_question.to_dict() if last_question else None
        # Запускаем асинхронно, чтобы пользователь сразу получил ответ.
        asyncio.create_task(add_questions_to_db(count.questions_num, session))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка сервера.")
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Мы не можем Вам прислать опрос, повторите запрос."
        )
    return question
