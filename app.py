import streamlit as st
import time
import gspread
from google.oauth2.service_account import Credentials


# =========================
# إعداد الصفحة
# =========================

st.set_page_config(
    page_title="FocusPulse 🧠",
    page_icon="🧠"
)

st.title("FocusPulse 🧠")
st.write("اختبار تجريبي لقياس تغيرات الأداء المرتبطة بالانتباه")

st.divider()


# =========================
# الاتصال بـ Google Sheets
# =========================

try:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    sheet = client.open("FocusPulse Results").sheet1

except Exception:
    sheet = None


# =========================
# بيانات المشارك
# =========================

if "name" not in st.session_state:
    st.session_state.name = ""

if "started" not in st.session_state:
    st.session_state.started = False

if "results" not in st.session_state:
    st.session_state.results = []

if "question_start" not in st.session_state:
    st.session_state.question_start = None


# =========================
# قبل البداية
# =========================

if not st.session_state.started:

    st.subheader("قبل أن نبدأ")

    st.write(
        "اكتبي اسم المشارك، ثم اضغطي على زر بدء الاختبار."
    )

    name = st.text_input(
        "اسم المشارك:",
        placeholder="اكتبي الاسم هنا"
    )

    if st.button("ابدأ التجربة 🧠"):

        if name.strip() == "":
            st.warning("اكتبي اسم المشارك أولًا.")

        else:
            st.session_state.name = name.strip()
            st.session_state.started = True
            st.session_state.results = []
            st.session_state.question_start = None

            st.rerun()


# =========================
# الأسئلة
# =========================

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
            "الجمعة"
        ),
    ]


    # =========================
    # عرض الأسئلة
    # =========================

    if len(st.session_state.results) < len(questions):

        i = len(st.session_state.results)

        question, options, correct = questions[i]

        if st.session_state.question_start is None:
            st.session_state.question_start = time.time()

        st.subheader(
            f"السؤال {i + 1} من {len(questions)}"
        )

        st.write(question)

        answer = st.radio(
            "اختاري إجابة:",
            options,
            index=None,
            key=f"question_{i}"
        )

        if st.button("التالي ➡️"):

            if answer is None:

                st.warning(
                    "اختاري إجابة أولًا قبل الانتقال للسؤال التالي."
                )

            else:

                reaction_time = (
                    time.time()
                    - st.session_state.question_start
                )

                correct_answer = answer == correct

                st.session_state.results.append({
                    "question": question,
                    "answer": answer,
                    "correct_answer": correct,
                    "reaction_time": reaction_time,
                    "correct": correct_answer
                })

                st.session_state.question_start = None

                st.rerun()


    # =========================
    # النتيجة النهائية
    # =========================

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

        correct_count = (
            len(st.session_state.results) - errors
        )

        average_time = (
            sum(times) / len(times)
        )

        score = (
            correct_count
            / len(questions)
            * 100
        )


        st.write(
            f"👤 اسم المشارك: {st.session_state.name}"
        )

        st.write(
            f"📊 النتيجة: {score:.0f}%"
        )

        st.write(
            f"⏱️ متوسط زمن الإجابة: {average_time:.2f} ثانية"
        )

        st.write(
            f"✅ عدد الإجابات الصحيحة: {correct_count}"
        )

        st.write(
            f"❌ عدد الأخطاء: {errors}"
        )


        # =========================
        # حفظ النتيجة في Google Sheets
        # =========================

        if sheet is not None:

            try:

                sheet.append_row([
                    st.session_state.name,
                    time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    round(score, 2),
                    round(average_time, 2),
                    correct_count,
                    errors
                ])

                st.success(
                    "تم حفظ نتيجة المشارك بنجاح في Google Sheets ✅"
                )

            except Exception:

                st.warning(
                    "تعذر حفظ النتيجة في Google Sheets حاليًا."
                )

        else:

            st.warning(
                "لم يتم الاتصال بـ Google Sheets."
            )


        # =========================
        # تقييم بسيط
        # =========================

        if average_time > 4 or errors >= 3:

            st.warning(
                "ظهر انخفاض في الأداء في هذه التجربة."
            )

        else:

            st.success(
                "الأداء كان مستقرًا في هذه التجربة."
            )


        # =========================
        # إعادة الاختبار
        # =========================

        if st.button("إعادة الاختبار 🔄"):

            st.session_state.started = False
            st.session_state.results = []
            st.session_state.question_start = None

            st.rerun()
