import streamlit as st
import time
import random

st.title("FocusPulse 🧠")
st.write("اختبار تجريبي لقياس تغيرات الأداء المرتبطة بالانتباه")

st.divider()

st.subheader("قبل أن نبدأ")
st.write(
    "اضغطي على الزر وابدئي الاختبار. "
    "حاولي الإجابة بأسرع ما تستطيعين وبدقة."
)

if "started" not in st.session_state:
    st.session_state.started = False

if "results" not in st.session_state:
    st.session_state.results = []

if "question_start" not in st.session_state:
    st.session_state.question_start = None

if st.button("ابدأ التجربة"):
    st.session_state.started = True
    st.session_state.results = []
    st.session_state.question_start = None
    st.rerun()


if st.session_state.started:

    questions = [
        (
            "إذا كان 15% من عدد ما يساوي 24، فما العدد؟",
            ["120", "140", "160", "180"],
            "160"
        ),
        (
            "ما العدد التالي في النمط؟ 3، 7، 15، 31، ؟",
            ["47", "55", "63", "67"],
            "63"
        ),
        (
            "أي كلمة تختلف عن البقية؟",
            ["كتاب", "قلم", "دفتر", "كرسي"],
            "كرسي"
        ),
        (
            "إذا كان 4 × 6 = 24، و 6 × 8 = 48، فما قيمة 8 × 10؟",
            ["64", "72", "80", "88"],
            "80"
        ),
        (
            "ما الحرف التالي؟ A, C, F, J, ؟",
            ["M", "N", "O", "P"],
            "O"
        ),
        (
            "عدد إذا أضفت إليه 12 ثم ضربت الناتج في 2 أصبح 50. ما العدد؟",
            ["11", "13", "15", "17"],
            "13"
        ),
        (
            "أي رقم يجب أن يحل محل علامة الاستفهام؟ 2، 6، 12، 20، 30، ؟",
            ["36", "40", "42", "44"],
            "42"
        ),
        (
            "إذا كانت جميع الورود أزهارًا، وبعض الأزهار حمراء، فهل نستطيع الجزم بأن بعض الورود حمراء؟",
            ["نعم", "لا", "دائمًا", "فقط إذا كانت صفراء"],
            "لا"
        ),
        (
            "ما العدد المختلف؟",
            ["16", "25", "36", "45"],
            "45"
        ),
        (
            "إذا كان اليوم الثلاثاء، فما اليوم بعد 45 يومًا؟",
            ["الأربعاء", "الخميس", "الجمعة", "السبت"],
            "الخميس"
        ),
    ]

    if len(st.session_state.results) < len(questions):

        i = len(st.session_state.results)
        question, options, correct = questions[i]

        if st.session_state.question_start is None:
            st.session_state.question_start = time.time()

        st.subheader(f"السؤال {i + 1} من {len(questions)}")
        st.write(question)

        answer = st.radio(
            "اختاري إجابة:",
            options,
            index=None,
            key=f"question_{i}"
        )

        if st.button("التالي"):

            if answer is None:
                st.warning("اختاري إجابة أولًا قبل الانتقال للسؤال التالي.")
            else:

                reaction_time = (
                    time.time() - st.session_state.question_start
                )

                correct_answer = answer == correct

                st.session_state.results.append({
                    "reaction_time": reaction_time,
                    "correct": correct_answer
                })

                st.session_state.question_start = None
                st.rerun()

    else:

        st.success("انتهى الاختبار 🎉")

        times = [
            x["reaction_time"]
            for x in st.session_state.results
        ]

        errors = sum(
            not x["correct"]
            for x in st.session_state.results
        )

        average_time = sum(times) / len(times)

        st.write(
            f"متوسط زمن الإجابة: {average_time:.2f} ثانية"
        )

        st.write(f"عدد الأخطاء: {errors}")

        if average_time > 4 or errors >= 3:
            st.warning(
                "ظهر انخفاض في الأداء في هذه التجربة."
            )
        else:
            st.success(
                "الأداء كان مستقرًا في هذه التجربة."
            )
