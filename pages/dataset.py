import requests
import streamlit as st
import json
import shutil
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from sqlalchemy import text
from menu import menu

menu()


def get_course():
    st.write("### Загрузка курсов")
    # headers = {"Authorization": "Bearer sk-SegLQz4AfKqK9o4reOmNNIarcbeOItWk"}
    res = requests.get(
        'http://synergyupgrade.loc:8092/neural/create')  # Создаём переменную, в которую сохраним код состояния запрашиваемой страницы.
    return json.loads(res.content)


def load_course():
    dataset = get_course()

    st.write("### Курсы")
    conn = st.connection('course_db', type='sql')
    with conn.session as s:
        # st.markdown(f"Note that `s` is a `{type(s)}`")
        # s.execute(text("CREATE TABLE IF NOT EXISTS prompts (id INTEGER, text TEXT, datetime TEXT);"))
        # s.execute(text("CREATE TABLE IF NOT EXISTS courses (id INTEGER, name_course TEXT);"))
        s.execute(text("DELETE FROM courses;"))
        s.execute(text("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'courses';"))
        # courses = {'1': 'course 1', '2': 'course 2', '3': 'course 3'}
        for item in dataset:
            s.execute(
                text('INSERT INTO courses ('
                     'course_id, name, description ,href , studyFormat, resultDocument, totalHours, duration, '
                     'studyProgrammeSection, whatYouLearnSection, whyLearnSection, numberVacancies, averageEarnings)'
                     'VALUES (:courseId, :name, :description ,:href , :studyFormat, :resultDocument, :totalHours,'
                     ':duration, :studyProgrammeSection, :whatYouLearnSection, :whyLearnSection, :numberVacancies, '
                     ':averageEarnings );'),
                params=dict(
                    courseId=item['courseId'],
                    name=item['name'],
                    description=item['description'],
                    href=item['href'],
                    studyFormat=item['studyFormat'],
                    resultDocument=item['resultDocument'],
                    totalHours=item['totalHours'],
                    duration=item['duration'],
                    studyProgrammeSection=item['studyProgrammeSection'],
                    whatYouLearnSection=item['whatYouLearnSection'],
                    whyLearnSection=item['whyLearnSection'],
                    numberVacancies=item['numberVacancies'],
                    averageEarnings=item['averageEarnings'],
                )
            )
        s.commit()


# for item in dataset:
# item1 = item['description'].replace('\r', '')
# st.write(f'{item1}')
# print(res.content)

# load_course()

chunk_size = st.text_input("Размер чанка", '1024', max_chars=4)

if not chunk_size.isalpha():
    st.write(chunk_size)
else:
    st.write('Please type in a int')

chunk_overlap = st.text_input("Перекрытие чанков", '100')
st.write("\n\r")


def re_index_db():
    create_dataset()
    f = open('dataset_paragraphs.txt', 'r', encoding='utf-8')
    # try:
    # with open('dataset_paragraphs.txt') as f:
    dataset = f.read()
    # finally:
    f.close()

    # Удалить индекс
    shutil.rmtree("faiss_index")
    #
    # loader = TextLoader(file_path, encoding='utf-8')
    # data = loader.load()
    #
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=100)
    #
    # # text_splitter = RecursiveCharacterTextSplitter()
    # documents = text_splitter.split_documents(data)
    source_chunks = []
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1028, chunk_overlap=100)

    for chunk in splitter.split_text(dataset):
        source_chunks.append(Document(page_content=chunk, metadata={}))

    # Initializing the embedding model
    # pip install sentence-transformers
    # pip install -U langchain-huggingface
    embeddings = OpenAIEmbeddings()
    # from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
    # from langchain_huggingface import HuggingFaceEmbeddings

    # pkl = db.serialize_to_bytes()  # serializes the faiss
    # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create an index db from separated text fragments
    db = FAISS.from_documents(source_chunks, embeddings)
    db.save_local("faiss_index")

    #

    # if not db:
    #     st.write("faiss_index не существует")
    #     db = FAISS.from_documents(source_chunks, embeddings)
    #     db.save_local("faiss_index")
    # db = FAISS.from_documents(source_chunks, embeddings)
    # db.save_local("faiss_index")

    return db


# if st.button('Загрузить курс'):
# load_course()

parametrs = {
    'name': {'name': 'Наименование курса', 'value': True, 'disabled': True},
    'course_id': {'name': 'Номер курса', 'value': True, 'disabled': True},
    'description': {'name': 'Описание курса', 'value': True, 'disabled': False},
    'href': {'name': 'Ссылка на курс', 'value': True, 'disabled': False},
    'studyFormat': {'name': 'Формат обучения', 'value': True, 'disabled': False},
    'resultDocument': {'name': 'Итоговый документ', 'value': True, 'disabled': False},
    'totalHours': {'name': 'Количество часов', 'value': True, 'disabled': False},
    'duration': {'name': 'Длительность обучения', 'value': True, 'disabled': False},
    'studyProgrammeSection': {'name': 'Программа обучения', 'value': True, 'disabled': False},
    'whatYouLearnSection': {'name': 'Чему вы научитесь?', 'value': True, 'disabled': False},
    'whyLearnSection': {'name': 'Зачем учиться на программе?', 'value': True, 'disabled': False},
    'numberVacancies': {'name': 'Количество вакансий от компаний', 'value': True, 'disabled': False},
    'averageEarnings': {'name': 'Средняя зарплата', 'value': True, 'disabled': False}
}

sections = {
    'course_id': 'Номер программы',
    'name': 'Программа',
    'description': 'Описание курса',
    'href': 'Cсылка(url) на курс',
    'studyFormat': 'Формат обучения',
    'resultDocument': 'Итоговый документ',
    'totalHours': 'Количество часов',
    'duration': 'Продолжительность обучения',
    'studyProgrammeSection': 'Программа обучения на курсе',
    'whatYouLearnSection': 'Чему вы научитесь на курсе',
    'whyLearnSection': 'Зачем учиться на курсе',
    'numberVacancies': 'Количество вакансий от компаний',
    'averageEarnings': 'Средняя зарплата',
}
checkbox_value = {
    'course_id': False,
    'name': False,
    'description': False,
    'href': False,
    'studyFormat': False,
    'resultDocument': False,
    'totalHours': False,
    'duration': False,
    'studyProgrammeSection': False,
    'whatYouLearnSection': False,
    'whyLearnSection': False,
    'numberVacancies': False,
    'averageEarnings': False,
}

with st.expander("Параметры"):
    fields = []
    for key, value in parametrs.items():
        checkbox_value[key] = st.checkbox(value['name'], value=value['value'], disabled=value['disabled'])
        if checkbox_value[key]:
            fields.append(key)


def getSection(course, field):
    match field:
        case 'course_id':
            return sections['course_id'] + ': ' + str(course[field])
        case 'name':
            return sections['name'] + ': ' + course[field]
        case 'description':
            return sections['description'] + ' ' + course['name'] + ': ' + course[field]
        case 'href':
            return sections['href'] + ' ' + course['name'] + ': ' + course[field]
        case 'studyFormat':
            return sections['studyFormat'] + ': ' + course[field]
        case 'resultDocument':
            return sections['resultDocument'] + ': ' + course[field]
        case 'totalHours':
            return sections['totalHours'] + ': ' + course[field]
        case 'duration':
            return sections['duration'] + ': ' + course[field]
        case 'studyProgrammeSection':
            return sections['studyProgrammeSection'] + ' ' + course['name'] + ': ' + course[field]
        case 'whatYouLearnSection':
            return sections['whatYouLearnSection'] + ' ' + course['name'] + ': ' + course[field]
        case 'whyLearnSection':
            return sections['whyLearnSection'] + ' ' + course['name'] + ': ' + course[field]
        case 'numberVacancies':
            return sections['numberVacancies'] + ': ' + course[field]
        case 'averageEarnings':
            return sections['averageEarnings'] + ': ' + course[field]


def create_paragraph(course, accepted_fields):
    paragraphs = []
    for field in accepted_fields:
        section = getSection(course, field).replace('\n\r', '').replace('\n', '')
        paragraphs.append(section)
    return '\n'.join(paragraphs)


def create_dataset():
    if fields:
        conn = st.connection('course_db', type='sql')
        courses = conn.query(f'select {", ".join(fields)} from courses limit 42', ttl=10)
        f = open('dataset_paragraphs.txt', 'w', encoding='utf-8')
        for index, row in courses.iterrows():
            paragraphs = create_paragraph(row, fields) + '\n\r'
            # st.write('\n\r')

            # try:
            # with open('dataset_paragraphs.txt') as f:
            f.write(paragraphs)
            # finally:
        f.close()
        # st.write(row['course_id'], '\n\r', row['name'] + '\n\r', row['description'] + '\n\r')


# if st.button('fetch'):
#     create_dataset()
st.write("\n\r")
if st.button('Реиндексировать'):
    re_index_db()
    st.write("Реиндексация прошла успешно!")
