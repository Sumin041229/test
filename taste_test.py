Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> def run_test():
...     questions = [
...         {
...             "text": "Q1. 혼자만의 시간이 주어진다면, 당신은 어디로 가고 싶나요?",
...             "choices": {
...                 "A": "햇살 들어오는 카페에서 조용히 책 읽기",
...                 "B": "지역 특색 있는 골목을 산책하며 가게 구경하기",
...                 "C": "은은한 조명의 바에서 잔잔한 음악 들으며 잔을 기울이기",
...                 "D": "아무 계획 없이 자연이나 공원에서 멍 때리기"
...             },
...             "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
...         },
...         {
...             "text": "Q2. 당신이 공간을 선택할 때 가장 먼저 반응하는 요소는?",
...             "choices": {
...                 "A": "조명이나 색감 같은 분위기",
...                 "B": "장소가 가진 이야기나 지역성",
...                 "C": "대화가 자연스레 이어질 수 있는 온기 있는 자리인지",
...                 "D": "조용하고 편안한 동선이나 구조"
...             },
...             "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
...         },
...         {
...             "text": "Q3. SNS에서 끌리는 피드 스타일은?",
...             "choices": {
...                 "A": "감성 일상 브이로그",
...                 "B": "숨은 동네 핫플 소개",
...                 "C": "잔잔한 대화와 웃음이 흐르는 모임 사진이나 술자리 브이로그",
...                 "D": "바다·산·자연 속 힐링 영상"
...             },
...             "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
...         },
...         {
...             "text": "Q4. 다음 중 가장 ‘끌리는’ 카페의 느낌은?",
...             "choices": {
                "A": "낮은 조도, LP 음악, 따뜻한 조명",
                "B": "오래된 골목 안, 간판 없는 로컬 카페",
                "C": "밤에도 오래 머무를 수 있고, 대화하기 좋은 아늑한 공간",
                "D": "나무 냄새 나는 테라스와 여백 많은 좌석"
            },
            "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
        },
        {
            "text": "Q5. 지금 당장 ‘회복’이 필요할 때 떠오르는 장소는?",
            "choices": {
                "A": "감정 정돈되는 분위기 있는 카페",
                "B": "동네 오래된 식당이나 골목길 산책",
                "C": "나를 잘 아는 친구와 마주 앉아 진심 나눌 수 있는 공간",
                "D": "조용하고 푸른 공간, 아무도 없는 벤치"
            },
            "categories": {"A": "감성", "B": "로컬", "C": "낭만", "D": "힐링"}
        }
    ]

    scores = {"감성": 0, "로컬": 0, "낭만": 0, "힐링": 0}

    print("🎯 당신의 취향을 탐색해보세요!\n")

    for q in questions:
        print(q["text"])
        for key, val in q["choices"].items():
            print(f"  {key}. {val}")
        answer = input("당신의 선택: ").strip().upper()
        while answer not in q["choices"]:
            answer = input("A, B, C, D 중에서 골라주세요: ").strip().upper()
        category = q["categories"][answer]
        scores[category] += 1
        print()

    total = sum(scores.values())
    print("✨ 당신의 취향 결과입니다:")
    for cat, val in scores.items():
        percent = (val / total) * 100
        print(f"- {cat}: {percent:.0f}%")

        
