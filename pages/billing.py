import streamlit as st

st.write("### Биллинг")
from menu import menu
menu()
# import pandas as pd
#
#
#
#
#
# # create form
# def add_dfForm():
#     row = pd.DataFrame({'Test_1': [Test_1],
#                         'Test_2': [Test_2],
#                         'Test_3': [Test_3]})
#     st.session_state.data = pd.concat([st.session_state.data, row])
#
#
# (placeholder_for_Test_1, placeholder_for_Test_2, placeholder_for_Test_3) = st.columns(3)
#
# disable_1 = True
# disable_2 = True
# disable_3 = True
#
# with placeholder_for_Test_1:
#     Test_1 = st.selectbox('Test_1', options=[0, 1, 2, 3])
#     if Test_1 == 0:
#         disable_1 = True
#     else:
#         disable_1 = False
# with placeholder_for_Test_2:
#     Test_2 = st.selectbox('Test_2', options=[0, 1, 2, 3], disabled=disable_1)
#     if Test_2 == 0:
#         disable_2 = True
#     else:
#         disable_2 = False
# with placeholder_for_Test_3:
#     Test_3 = st.selectbox('Test_3', options=[0, 1, 2, 3], disabled=disable_2)
#     if Test_3 == 0:
#         disable_3 = True
#     else:
#         disable_3 = False
#
# dfForm = st.form(key='dfForm')
#
# with dfForm:
#     placeholder_for_Test_1 = st.empty()
#     placeholder_for_Test_2 = st.empty()
#     placeholder_for_Test_3 = st.empty()
#     add_button = st.form_submit_button("Add", on_click=add_dfForm, type="primary",
#                                        disabled=disable_3)
# # create user dataframe
# if 'data' not in st.session_state:
#     data = pd.DataFrame({'Test_1': [], 'Test_2': [], 'Test_3': []})
#     st.session_state.data = data
#
#
# def callback():
#     edited_rows = st.session_state["data_editor"]["edited_rows"]
#     rows_to_delete = []
#
#     for idx, value in edited_rows.items():
#         if value["x"] is True:
#             rows_to_delete.append(idx)
#
#     st.session_state["data"] = (
#         # st.session_state["data"].drop(axis=0, inplace=True).reset_index(drop=True)
#         st.session_state["data"].drop(rows_to_delete, axis=0).reset_index(drop=True)
#     )
#
#
# columns = st.session_state["data"].columns
# column_config = {column: st.column_config.Column(disabled=True) for column in columns}
#
# modified_df = st.session_state["data"].copy()
# modified_df["x"] = False
# # Make Delete be the first column
# modified_df = modified_df[["x"] + modified_df.columns[:-1].tolist()]
#
# st.data_editor(
#     modified_df,
#     key="data_editor",
#     on_change=callback,
#     hide_index=True,
#     column_config=column_config,
# )



