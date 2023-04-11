# Chromatica-FastAPI

FastAPI + Stable diffusion model

| 이모지 | 설명 |
| --- | --- |
| :art: | 코드의 구조/형태 개선 |
| :zap: | 성능 개선 |
| :fire: | 코드/파일 삭제 |
| :bug: | 버그 수정 |
| :ambulance: | 긴급 수정 |
| :sparkles: | 새 기능 |
| :memo: | 문서 추가/수정 |
| :lipstick: | UI/스타일 파일 추가/수정 |
| :tada: | 프로젝트 시작 |
| :white_check_mark: | 테스트 추가/수정 |
| :lock: | 보안 이슈 수정 |
| :bookmark: | 릴리즈/버전 태그 |
| :green_heart: | CI 빌드 수정 |
| :pushpin: | 특정 버전 의존성 고정 |
| :construction_worker: | CI 빌드 시스템 추가/수정 |
| :chart_with_upwards_trend: | 분석, 추적 코드 추가/수정 |
| :recycle: | 코드 리팩토링 |
| :heavy_plus_sign: | 의존성 추가 |
| :heavy_minus_sign: | 의존성 제거 |
| :wrench: | 구성 파일 추가/삭제 |
| :hammer: | 개발 스크립트 추가/수정 |
| :globe_with_meridians: | 국제화/현지화 |
| :poop: | 똥싼 코드 |
| :rewind: | 변경 내용 되돌리기 |
| :twisted_rightwards_arrows: | 브랜치 합병 |
| :package: | 컴파일된 파일 추가/수정 |
| :alien: | 외부 API 변화로 인한 수정 |
| :truck: | 리소스 이동, 이름 변경 |
| :page_facing_up: | 라이센스 추가/수정 |
| :bulb: | 주석 추가/수정 |
| :beers: | 술 취해서 쓴 코드 |
| :card_file_box: | 데이터베이스 관련 수정 |
| :loud_sound: | 로그 추가/수정 |
| :see_no_evil: | .gitignore 추가/수정 |

## Directory structure

```
├── main.py
├── setup.py
├── environment.yaml
├── LICENSE
│ 
├── 📁 config
├── 📁 app
│ 	├── __init__.py
│	└── generate.py
│
├── 📁 ldm
├── 📁 models
├── 📁 optimizedSD
├── 📁 input
│ 	├── 📁 img2img
│	└── 📁 inpaint
│ 	    ├── 📁 base_image
│	    └── 📁 mask_image
├── 📁 output
│ 	├── 📁 img2img
│	└── 📁 inpaint
│
└── README.md
```
