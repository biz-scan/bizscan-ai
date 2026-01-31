import logging

# 로거 생성
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# 핸들러 설정 (콘솔 출력)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)