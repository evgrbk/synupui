from sqlalchemy import text
import streamlit as st
from datetime import timedelta
# from schedule import every, repeat, run_pending
from menu import menu
menu()

# st.set_page_config(
#     page_title='Редактирование промта'
# )

# st.title('Системные промты')
st.write("### промты")
conn = st.connection('course_db', type='sql')
# with conn.session as s:
#     st.markdown(f"Note that `s` is a `{type(s)}`")
#     s.execute(text("CREATE TABLE IF NOT EXISTS prompts (id INTEGER, text TEXT, datetime TEXT);"))
#
#
#     s.commit()

# courses = conn.query('select * from courses', ttl=timedelta(minutes=10))
# st.dataframe(courses)
prompts = conn.query('select text, datetime from prompts', ttl=10)
st.dataframe(
    prompts,
    hide_index=True,
    column_config={
        "text": "Промт",  # change the title
        "datetime": "Дата создания"
    }
)


