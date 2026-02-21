# 🔎 BizScan
**공공데이터 + AI로 완성하는 소상공인 맞춤형 비즈니스 컨설팅 웹 서비스, 비즈스캔**
<br><br>
  
2025.12.28 ~ 2026.02.20
<br><br>

[![Project Link](https://img.shields.io/badge/🌐%20Project%20Site-bizscan-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://bizscan-web.vercel.app/)
<br><br>


### 💡 프로젝트 요약
**서비스 개요**
> BizScan은 공공 상권 데이터를 AI가 분석하여  
소상공인에게 **즉시 실행 가능한 전략(Action Plan)** 을 제공하는  
실행 중심 비즈니스 컨설팅 웹 서비스입니다.

> 기존 상권 분석 서비스가 “데이터 시각화”에 그쳤다면, BizScan은 **데이터 → 인사이트 → 실행 전략**까지 연결합니다.

**문제 정의**  
> 상권 데이터는 많지만,
소상공인이 실제로 무엇을 해야 하는지에 대한 구체적인 전략은 부족합니다.

**BizScan의 Solution**
> **데이터 → 인사이트 → 실행 전략(Action Plan)**  

> BizScan은 분석에서 그치지 않고
실행까지 이어지는 **AI 상권 컨설턴트**를 목표로 합니다.

<br><br>

### 🚀 Service Goals

#### [1] AI 상권 스캐너
> 공공데이터와 지역 정보를 자동 수집 및 분석하여 가게 현황을 한눈에 제공

#### [2] 실행형 AI 리포트 
> SWOT 기반 분석 + 구체적인 실행 전략 제시

#### [3] 소상공인의 성장 루트 설계
> 실행 → 기록 → 성과 확인 → 재분석  
지속 가능한 비즈니스 개선 구조

<br><br>

## Backend Overview
> BizScan Backend는 Spring Boot 기반 API 서버와 FastAPI 기반 AI 서버로 구성됩니다.

### Backend Core Features
```
🔐 JWT 기반 인증
🏪 매장 정보 CRUD
📊 상권 데이터 수집 및 저장 (RDB + VectorDB)
🤖 AI SWOT 리포트 및 실행 전략 생성
📈 실행 관리 및 성과 추적
🚀 Docker 기반 CI/CD 자동 배포
```

### Infrastructure & DevOps
```
• CI/CD 파이프라인 최적화 (GitHub Actions + Self-hosted Runner)
• Prometheus + Grafana 기반 모니터링 시스템 구축
• Redis 캐시 도입 (JWT Refresh Token 관리 및 조회 성능 개선)
• Nginx 기반 HTTPS 도메인 연결 및 SSL 적용
• Docker 기반 컨테이너 환경 구성
```
<br><br>

## System Architecture
<img width="1010" height="795" alt="최종 인프라 구성도" src="https://github.com/user-attachments/assets/4df198b9-569b-4434-a568-39998af9eeec" />
<br><br>


## ERD
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/dfc8b9bc-5618-41fa-866d-395519d2cfe2" />
<br><br>


### Contributors

> 공공 상권 데이터를 기반으로 AI 분석 시스템을 설계하고,  
> 실행 가능한 비즈니스 전략을 제공하는 BizScan 팀입니다.



| PM | Design |
|:---:|:---:|
| [최근영](https://github.com/rmsdud7763) | [이연수](https://github.com/이연수) |
| <img src="https://avatars.githubusercontent.com/rmsdud7763" width="150" /> | <img src="https://github.githubassets.com/images/spinners/transparent.gif" width="150" /> |



| FE Developer | FE Developer | FE Developer |
|:---:|:---:|:---:|
| [김도형](https://github.com/dohyung001) | [박하은](https://github.com/prkhaeun) | [백수민](https://github.com/suminn01) |
| <img src="https://avatars.githubusercontent.com/dohyung001" width="150" /> | <img src="https://avatars.githubusercontent.com/prkhaeun" width="150" /> | <img src="https://avatars.githubusercontent.com/suminn01" width="150" /> |



| BE Developer | BE Developer | BE Developer | BE Developer | BE Developer |
|:---:|:---:|:---:|:---:|:---:|
| [김종혁](https://github.com/kjh015) | [신채린](https://github.com/shinchaerin79) | [김가빈](https://github.com/gcongK) | [편선아](https://github.com/Seona12) | [윤수정](https://github.com/Yoonssu) |
| <img src="https://avatars.githubusercontent.com/kjh015" width="150" /> | <img src="https://avatars.githubusercontent.com/shinchaerin79" width="150" /> | <img src="https://avatars.githubusercontent.com/gcongK" width="150" /> | <img src="https://avatars.githubusercontent.com/Seona12" width="150" /> | <img src="https://avatars.githubusercontent.com/Yoonssu" width="150" /> |

<br><br>


## Stacks  

### Design (UI/UX)
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)
![Styled Components](https://img.shields.io/badge/Styled%20Components-DB7093?style=for-the-badge&logo=styled-components&logoColor=white)
![Adobe Photoshop](https://img.shields.io/badge/adobe%20photoshop-%2331A8FF.svg?style=for-the-badge&logo=adobe%20photoshop&logoColor=white)

### Frontend
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-4B32C3?style=for-the-badge&logo=vite&logoColor=white)
![axios](https://img.shields.io/badge/axios-007ACC?style=for-the-badge&logo=axios&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

### Backend
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white)
![Spring Security](https://img.shields.io/badge/Spring%20Security-4A5B6D?style=for-the-badge&logo=spring-security&logoColor=white)
![Spring Data JPA](https://img.shields.io/badge/Spring%20Data%20JPA-5D8AA8?style=for-the-badge&logo=spring-data&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-FF4438?style=for-the-badge&logo=redis&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-000000?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-FF4F8B?style=for-the-badge)
![Dozzle](https://img.shields.io/badge/Dozzle-000000?style=for-the-badge)

### Communication
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)

<br><br>
## 협업 규칙

### 1) Git 브랜치 전략
- `main` : 배포용(항상 안정 상태 유지)
- `develop` : 개발 통합 브랜치
- `feature/#이슈번호-기능명` : 기능 개발
- `fix/#이슈번호-버그명` : 버그 수정
- `refactor/#이슈번호-내용` : 리팩토링
- `deploy/#이슈번호-내용` : 배포
<br>

### 2) 프로젝트 구조 결정 (FastAPI 기준)
- 레이어 기반 구조로 구성 (routers / schemas / services 중심)
- 배포/실행 관련 파일은 docker/ 폴더로 분리 (Dockerfile, docker-compose.yml, .env.example)
<br>

### 3) 코드 컨벤션 (Python/FastAPI)
- 네이밍 규칙  
  - 파일/폴더: snake_case  
  - 함수/변수: snake_case  
  - 클래스/Pydantic 모델: PascalCase  
  - 상수/환경변수 키: UPPER_SNAKE_CASE  
- 레이어 책임 분리  
  - routers는 요청/응답 처리 중심 (파라미터 검증, 의존성 주입, 서비스 호출)  
  - 비즈니스 로직은 services에 위치 (AI 호출, 데이터 처리/정제 등)  
  - 데이터 스키마는 schemas로만 관리 (요청/응답 DTO 일원화)  

#### 🎯 Git Commit Convention
```
  🎉 Start: Start New Project [:tada]  
  ✨ Feat: 새로운 기능을 추가 [:sparkles]  
  🐛 Fix: 버그 수정 [:bug]  
  🎨 Design: CSS 등 사용자 UI 디자인 변경 [:art]  
  ♻️ Refactor: 코드 리팩토링 [:recycle]  
  🔧 Settings: Changing configuration files [:wrench]  
  🗃️ Comment: 필요한 주석 추가 및 변경 [:card_file_box]  
  ➕ Dependency/Plugin: Add a dependency/plugin [:heavy_plus_sign]  
  📝 Docs: 문서 수정 [:memo]  
  🔀 Merge: Merge branches [:twisted_rightwards_arrows:]  
  🚀 Deploy: Deploying stuff [:rocket]  
  🚚 Rename: 파일 혹은 폴더명을 수정하거나 옮기는 작업만인 경우 [:truck]  
  🔥 Remove: 파일을 삭제하는 작업만 수행한 경우 [:fire]  
  ⏪️ Revert: 전 버전으로 롤백 [:rewind]
```

<br>

### 4) PR 규칙
- PR은 **작게**(기능 단위) 올리기
- PR 템플릿 사용:
  - 관련 이슈 연결: `Close #이슈번호`
  - 변경 내용 요약 작성
  - 테스트/검증 내용 작성(가능하면 스크린샷/로그 포함)
- 최소 **1명 이상 리뷰 승인 후 머지**
- 머지는 원칙적으로 `Squash and merge` (커밋 히스토리 정리)
