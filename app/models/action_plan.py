from sqlalchemy import Column, Integer, BigInteger, String, Text, Enum, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.action_plan_enum import CategoryEnum


# 실행전략 (action_plan) 테이블
class ActionPlan(Base):
    __tablename__ = "action_plan"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    swot_id = Column(BigInteger, ForeignKey("swot.id"), nullable=False)
    title = Column(String(255), nullable=True)
    category = Column(Enum(CategoryEnum), nullable=True)
    tags = Column(JSON, nullable=True)
    reason = Column(Text, nullable=True)

    # 1 : N 관계 (세부 실행전략)
    details = relationship(
        "ActionDetail",
        back_populates="action_plan",
        cascade="all, delete-orphan"
    )

# 세부 실행전략 (action_detail) 테이블
class ActionDetail(Base):
    __tablename__ = "action_detail"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    action_plan_id = Column(BigInteger, ForeignKey("action_plan.id"), nullable=False)
    content = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=True)

    # N : 1 관계 (실행전략)
    action_plan = relationship("ActionPlan", back_populates="details")