import streamlit as st
import time

st.title("FocusPulse 🧠")
st.write("اختبار تجريبي لقياس تغيرات الأداء المرتبطة بالانتباه")

st.divider()

st.subheader("قبل أن نبدأ")
st.write("اضغطي على الزر وابدئي الاختبار. حاولي الإجابة بأسرع ما تستطيعين وبدقة.")

if "started" not in st.session_state:
    st.session_state.started = False

if "results" not in st.session_state:
    st.session_state.results = []

if st.button("ابدأ التجربة"):
    st.session_state.started = True
    st.session_state.results = []
    st.rerun()

if st.session_state.started:

    questions = [
        ("كم يساوي 7 + 5؟", ["10", "12", "14"], "12"),
        ("كم يساوي 9 × 3؟", ["18", "27", "30"], "27"),
        ("ما الحرف التالي؟ A, B, C, ؟", ["D", "E", "F"], "D"),
        ("كم يساوي 20 - 8؟", ["10", "12", "14"], "12"),
        ("كم يساوي 6 × 4؟", ["20", "24", "28"], "24"),
    ]

    if len(st.session_state.results) < len(questions):

        i = len(st.session_state.results)
        question, options, correct = questions[i]

        if "question_start" not in st.session_state:
            st.session_state.question_start = time.time()

        st.subheader(f"السؤال {i + 1} من {len(questions)}")
        st.write(question)

        answer = st.radio(
            "اختاري إجابة:",
            options,
            key=f"question_{i}"
        )

        if st.button("التالي"):
            reaction_time = time.time() - st.session_state.question_start
            correct_answer = answer == correct

            st.session_state.results.append({
                "reaction_time": reaction_time,
                "correct": correct_answer
            })

            st.session_state.question_start = time.time()
            st.rerun()

    else:

        st.success("انتهى الاختبار 🎉")

        times = [x["reaction_time"] for x in st.session_state.results]
        errors = sum(not x["correct"] for x in st.session_state.results)
        average_time = sum(times) / len(times)

        st.write(f"متوسط زمن الإجابة: {average_time:.2f} ثانية")
        st.write(f"عدد الأخطاء: {errors}")

        if average_time > 3 or errors >= 2:
            st.warning("ظهر انخفاض في الأداء في هذه التجربة.")
        else:
            st.success("الأداء كان مستقرًا في هذه التجربة.")
