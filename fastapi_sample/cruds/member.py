from fastapi_sample import models

from .base import BaseRepository


class MemberRepository(BaseRepository):
    def delete_member(self, member: models.Member):
        self.session.delete(member)
        self.session.commit()
