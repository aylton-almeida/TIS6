from __future__ import annotations


class Question:

    is_answered: bool
    title: str
    link: str

    def __init__(self, data: dict) -> None:
        self.is_answered = data.get('is_answered')
        self.title = data.get('title')

    @staticmethod
    def from_exchange(data: dict) -> Question:
        return Question({
            'title': data.get('title'),
            'is_answered': data.get('is_answered'),
            'link': data.get('link')
        })
