from sqlalchemy import text
import streamlit as st
from datetime import timedelta
# from schedule import every, repeat, run_pending

st.set_page_config(
    page_title='Редактирование промта'
)

# st.title('Системные промты')
st.write("### промты")
conn = st.connection('course_db', type='sql')
with conn.session as s:
    # st.markdown(f"Note that `s` is a `{type(s)}`")
    s.execute(text("CREATE TABLE IF NOT EXISTS prompts (id INTEGER, text TEXT, datetime TEXT);"))
    s.execute(text("CREATE TABLE IF NOT EXISTS courses (id INTEGER, name_course TEXT);"))
    s.execute(text("DELETE FROM courses;"))
    courses = {'1': 'course 1', '2': 'course 2', '3': 'course 3'}
    for k in courses:
        s.execute(
            text('INSERT INTO courses (id, name_course) VALUES (:id, :name_course);'),
            params=dict(id=k, name_course=courses[k])
        )
    s.commit()

# courses = conn.query('select * from courses', ttl=timedelta(minutes=10))
# st.dataframe(courses)
prompts = conn.query('select text, datetime from prompts', ttl=10)
st.dataframe(
    prompts,
    column_config={
        "text": "Промт",  # change the title
        "Дата создания": "Промт"
    }
)

# container = st.beta_container()
# for i in range(0, len(df), 50):
#     container.dataframe(df[i:i+50])
# from streamlit.report_thread import get_report_ctx
# Add a button to refresh the page
# if st.button('Refresh'):
#     ctx = get_report_ctx()
#     session_id = ctx.session_id
#     st.experimental_rerun()
#     st.stop()
# st.rerun()
# from streamlit.script_runner import StopException, RerunException
# if st.button('refresh'):

    # raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
    # st.markdown('<script>window.location.reload(true);</script>', unsafe_allow_html=True)
    # prompts = conn.query('select text, datetime from prompts', ttl=10)
    # st.table(prompts)
    # prompts = conn.query('select COUNT(*) from prompts', ttl=timedelta(minutes=10))
    # st.write(f"{prompts}")
    # st.dataframe(
    #     prompts,
    #     column_config={
    #         "text": "Промт",  # change the title
    #         "Дата создания": "Промт"
    #     }
    # )
    # st.rerun()
