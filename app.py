import streamlit as st
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# הגדרת כיוון כתיבה כללי לאתר
st.set_page_config(page_title="Tomash Finance", layout="wide")

# פונקציות תיקון עברית לגרפים
def fix_g(text):
    return get_display(arabic_reshaper.reshape(str(text)))

# --- עיצוב ותפריט צד ---
st.title("💎 Tomash Finance - דאשבורד השקעות")
st.sidebar.header("הגדרות מחשבון")

tool = st.sidebar.selectbox("בחר כלי ניתוח:", 
    ['צמיחה והשוואה', 'תזרים REIT', 'ניתוח משכנתא', 'אוכל דמי הניהול', 'מחשבון יעדים'])

# --- קליטת נתונים דינמית ---
p = st.sidebar.number_input("סכום בסיס (₪):", value=100000)
y = st.sidebar.slider("תקופה (שנים):", 1, 30, 15)
r = st.sidebar.slider("תשואה/ריבית שנתית (%):", 0.0, 20.0, 8.0) / 100

# --- לוגיקה והצגת תוצאות ---
col1, col2 = st.columns([1, 1])

with col1:
    if tool == 'צמיחה והשוואה':
        d = st.sidebar.number_input("הפקדה חודשית (₪):", value=2000)
        # לוגיקה (זהה למה שבנינו)
        balance = p
        history = [p]
        for _ in range(y * 12):
            balance = (balance + d) * (1 + (r/12))
            history.append(balance)
        
        st.metric("הון סופי מוערך", f"₪{balance:,.0f}")
        fig, ax = plt.subplots()
        ax.plot(history, color='#2ecc71')
        ax.set_title(fix_g("תחזית צמיחה"))
        st.pyplot(fig)

    elif tool == 'תזרים REIT':
        # חישוב תזרים מניות REIT להכנסה חודשית
        m_net = (p * (r/12)) * (1 - 0.25)
        st.metric("הכנסה חודשית נטו (אחרי מס)", f"₪{m_net:,.0f}")
        st.write("מחשבון זה מותאם למניות ריט בישראל עם הנחת מס קבועה.")


# המשך שאר הפיצ'רים (משכנתא, דמי ניהול וכו') באותו מבנה...
