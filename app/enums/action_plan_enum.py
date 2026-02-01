import enum

# 실행전략 카테고리 Enum 정의
class CategoryEnum(str, enum.Enum):
    MARKETING = "마케팅"
    MENU = "메뉴"
    OPERATION = "운영"