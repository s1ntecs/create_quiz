from typing import List
from fastapi import Depends
from models.quiz import Question

import httpx


async def get_questions_data(count: int) -> List[dict]:
    async with httpx.AsyncClient() as client:
        url = f"https://jservice.io/api/random?count={count}"
        response = await client.get(url)
        if response.status_code != 200:
            return {}
        data = response.json()
    return data


async def add_questions_to_db(count: int, session: Depends):
    questions_data = await get_questions_data(count)
    for question_data in questions_data:
        question_exist = (session.query(Question).filter(
                          Question.question_id == question_data["id"])
                          .first()
                          )
        while question_exist:
            questions_data = await get_questions_data(1)
            question_data = questions_data[0]
            question_exist = (session.query(Question).filter(
                              Question.question_id == question_data["id"])
                              .first())
        question = Question(question_id=question_data["id"],
                            question=question_data["question"],
                            answer=question_data["answer"],
                            created_at=question_data["created_at"]
                            )
        session.add(question)
    session.commit()
