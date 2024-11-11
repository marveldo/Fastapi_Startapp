from sqlalchemy import (
    ForeignKey ,
    String ,
    DateTime,
    Column
)
from ..models.BaseModel import BaseModel
from sqlalchemy.orm import relationship
from app.models.Basemanager import BaseManager

class OutStandingTokens(BaseModel):

    __tablename__ = 'refresh_tokens' 

    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token = Column(String, unique=True, nullable=False)

    expires_in = Column(DateTime , nullable=False)

    user = relationship("User", back_populates="token")



class BlacklistedTokens(BaseModel):
    __tablename__ = 'blacklisted_tokens' 

    token = Column(
        String , nullable=False
    )




    