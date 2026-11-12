# Science Class by Teacher 노글라쓰

수업에서 쓰는 과학 시뮬레이션입니다. 첫 화면에서 시뮬레이션을 골라 엽니다.

- `index.html` — 첫 화면 (칠판 배경, 생명과학·지구과학 줄에 시뮬레이션을 나란히 배치)
- `life-science/nephron.html` — 콩팥의 구조와 기능
- `earth-science/diurnal.html` — 천체의 일주운동 시뮬레이션
- `earth-science/sun-annual.html` — 태양의 연주운동 3D 시뮬레이션
- `earth-science/moon-phases.html` — 달의 위상 변화 관찰 시뮬레이션

`life-science/index.html`, `earth-science/index.html`은 첫 화면의 해당 과목 줄로 넘겨 주는 페이지입니다.

맨 위에 남아 있는 `diurnal.html`, `sun-annual.html`, `moon-phases.html`은 예전 주소로 들어온 사람을 `earth-science/` 안의 새 주소로 넘겨 주는 페이지입니다.

새 시뮬레이션은 과목 폴더에 넣고 첫 화면의 해당 과목 줄에 쪽지를 하나 추가합니다. 새 과목은 폴더를 만들고 첫 화면에 줄을 하나 더 추가합니다.

## 원본 시뮬레이션 자동 반영

시뮬레이션 원본은 Claude 아티팩트입니다. `sync/sources.json`에 원본 주소와 사이트 파일이 짝지어져 있고,
`sync/build.py`가 원본을 사이트 파일로 옮깁니다(원본은 그대로 두고 `lang="ko"`와 '⌂ 처음으로' 버튼만 더함).
원본의 제목이 바뀌면 이 사이트 첫 화면과 메인페이지(dajihoya/NOHclass)의 카드 제목도 함께 바뀝니다.
예약 작업이 주기적으로 원본을 확인해 바뀐 것만 올립니다.
