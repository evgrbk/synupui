# pip install langchain-community
# pip install langchain-openai

import streamlit as st
import os
import getpass
import re
import json
import requests
from datetime import datetime, timedelta, timezone
# from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
# from langchain.embeddings.openai import OpenAIEmbeddings
import openai
# from langchain.llms import OpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

# from langchain_openai import ChatOpenAI,OpenAIEmbedding
# from langchain_community.chat_models import ChatOpenAI
# from langchain_community.llms import OpenAI
# LL_MODEL = "gpt-3.5-turbo-0613"
# print(f'LL_MODEL = {LL_MODEL}')
# openai.api_key = getpass.getpass("Введите OpenAi API key:")
# from gtts import gTTS
# from playsound import playsound
# text_sp = input("Введите текст для воспроизведения \n>>> ")
# language = 'ru'
# s = gTTS(text_sp, lang=language, slow=False)
# s.save(os.path.abspath('./sample.mp3'))
# playsound(os.path.abspath('./sample.mp3'))

# from mutagen.mp3 import MP3
# import time
# import miniaudio
#
# file='1.mp3'
# audio = MP3(file)
# length=audio.info.length
# stream = miniaudio.stream_file(file)
#
# with miniaudio.PlaybackDevice() as device:
#     device.start(stream)
#     print('playing')
#     time.sleep(length)
openai.api_key = "sk-84kAJqBm1S2hQQArg8JZxD74RYV3SXso"  #
os.environ["OPENAI_API_KEY"] = openai.api_key
openai.base_url = "https://api.proxyapi.ru/openai/v1"
os.environ["OPENAI_BASE_URL"] = openai.base_url
#
# # Промт
# system = '''You are the administrator of the food ordering chat and you answer customer questions in the chat. Never rush to answer,
# carefully read the terms of the question and give an accurate and detailed answer, focusing on the minimum and maximum cost of the dish.
# Report prices only from the transferred document, do not name prices from yourself.
# You have a document with information about all restaurants, the menu of these restaurants, dishes and prices.
# Do not mention the document or its fragments when answering, the client does not need to know anything about
# the document you are using to prepare a response.
# Answer so that the person wants to place an order.
# Answer all questions only in Russian'''
#
# system = '''Вы являетесь администратором образовательного маркетплейса Synergy Upgrade и отвечаете на вопросы клиентов в чате. Никогда не спешите с ответом,
# внимательно прочитайте условия вопроса и дайте точный ответ, ориентируясь на ключевые слова в запросе.
# Используйте данные только из переданного документа, не используйте данные от себя.
# У вас есть документ с информацией обо всех образовательных программах маркетплейса Synergy Upgrade ресторанах, номерах программ, ссылках и описании.
# Не упоминайте документ или его фрагменты при ответе, клиенту не обязательно что-либо знать о
# документе, который вы используете для подготовки ответа.
# В ответе указывай до 5 программ и используй только формат: "Номер программы;" через запятую.
# #
# # Отвечайте на все вопросы только на русском языке'''
skill_level = ''
wishes = ''
system = '''Вы являетесь администратором образовательного маркетплейса Synergy Upgrade и отвечаете на вопросы клиентов в чате. Никогда не спешите с ответом,
внимательно прочитайте условия вопроса и дайте точный ответ, ориентируясь на ключевые слова в запросе, учитывая, что текущий уровень знаний клиента: ''' + skill_level + ''',
а особые пожелания клиента: ''' + wishes + '''.
Используйте данные только из переданного документа, не используйте данные от себя.
У вас есть документ с информацией обо всех образовательных программах маркетплейса Synergy Upgrade ресторанах, номерах программ, ссылках и описании.
Не упоминайте документ или его фрагменты при ответе, клиенту не обязательно что-либо знать о
документе, который вы используете для подготовки ответа.
В ответе указывай до 5 программ и используй только формат: "Номер программы; Твой комментарий о программе; Ссылка на курс" через запятую.

Отвечайте на все вопросы только на русском языке'''
#
# База знаний, фрагмент
database = '''
программа: Интернет-маркетинг
Номер программы Интернет-маркетинг: 18
ссылка(url) курса Интернет-маркетинг на сайте https://synergyupgrade.ru: https://synergyupgrade.ru/product/internet-marketing-18
Зачем учиться на Интернет-маркетолога: Специалист по интернет-маркетингу настраивает рекламные кампании и оценивает эффективность продвижения продукта. Профессия интернет-маркетолог самая востребованная и перспективная профессия нашего времени.

программа: Frontend-разработчик
Номер программы Frontend-разработчик: 661
ссылка(url) курса Frontend-разработчик на сайте https://synergyupgrade.ru: https://synergyupgrade.ru/product/frontend-razrabotchik-661
Зачем учиться на Frontend-разработчик: Множество компаний реализуют веб-проекты, которые требуют понятного и удобного интерфейса. Для его разработки к работе привлекаются грамотные frontend-специалисты. Именно поэтому эта специальность востребована как в России, так и за рубежом.

программа: SMM-маркетинг
Номер программы SMM-маркетинг: 680
ссылка(url) курса SMM-маркетинг на сайте https://synergyupgrade.ru: https://synergyupgrade.ru/product/kurs-smm-marketing-680
Зачем учиться на SMM-маркетинг: Соцсети нужны почти каждой компании, которая хочет развиваться и собирать новую аудиторию. Задача SММ-специалиста - ненавязчиво направить подписчиков на выполнение необходимого для работодателя целевого действия.

Программа: Яндекс.Метрика для бизнеса
Номер программы Яндекс.Метрика для бизнеса: 2245
Cсылка(url) курса Яндекс.Метрика для бизнеса: https://synergyupgrade.ru/product/yandeks-metrika-dlya-biznesa-2245

Программа: Стиль, как часть личного бренда
Номер программы Стиль, как часть личного бренда: 3036
Cсылка(url) курса Стиль, как часть личного бренда: https://synergyupgrade.ru/product/stil-kak-chast-lichnogo-brenda-3036

Программа: Цифровые медиакоммуникации: ведение официальных страниц органов власти в социальных сетях
Номер программы Цифровые медиакоммуникации: ведение официальных страниц органов власти в социальных сетях: 3037
Cсылка(url) курса Цифровые медиакоммуникации: ведение официальных страниц органов власти в социальных сетях: https://synergyupgrade.ru/product/cifrovye-mediakommunikacii-vedenie-oficialnyh-stranic-organov-vlasti-v-socialnyh-setyah-3037

Программа: Искусственный интеллект в маркетинге
Номер программы Искусственный интеллект в маркетинге: 3129
Cсылка(url) курса Искусственный интеллект в маркетинге: https://synergyupgrade.ru/product/iskusstvennyj-intellekt-v-marketinge-3129

Программа: Маркетинг лояльности
Номер программы Маркетинг лояльности: 3130
Cсылка(url) курса Маркетинг лояльности: https://synergyupgrade.ru/product/marketing-loyalnosti-3130

Программа: Спортивный маркетинг
Номер программы Спортивный маркетинг: 3002
Cсылка(url) курса Спортивный маркетинг: https://synergyupgrade.ru/product/sportivnyj-marketing-2932-3002

Программа: Психология личного бренда
Номер программы Психология личного бренда: 3016
Cсылка(url) курса Психология личного бренда: https://synergyupgrade.ru/product/psihologiya-lichnogo-brenda-3016

Программа: Продакт-плейспент
Номер программы Продакт-плейспент: 3017
Cсылка(url) курса Продакт-плейспент: https://synergyupgrade.ru/product/prodakt-plejspent-3017

Программа: Архетипы клиентов
Номер программы Архетипы клиентов: 3018
Cсылка(url) курса Архетипы клиентов: https://synergyupgrade.ru/product/arhetipy-klientov-3018

Программа: Запуск интернет магазина с нуля
Номер программы Запуск интернет магазина с нуля: 3033
Cсылка(url) курса Запуск интернет магазина с нуля: https://synergyupgrade.ru/product/zapusk-internet-magazina-s-nulya-3033

Программа: Как продавать на маркетплейсах
Номер программы Как продавать на маркетплейсах: 3034
Cсылка(url) курса Как продавать на маркетплейсах: https://synergyupgrade.ru/product/kak-prodavat-na-marketplejsah-3034

Программа: Продвижение на маркетплейсах
Номер программы Продвижение на маркетплейсах: 3045
Cсылка(url) курса Продвижение на маркетплейсах: https://synergyupgrade.ru/product/prodvizhenie-na-marketplejsah-3045

Программа: Интернет-маркетолог E-commerce
Номер программы Интернет-маркетолог E-commerce: 3046
Cсылка(url) курса Интернет-маркетолог E-commerce: https://synergyupgrade.ru/product/internet-marketolog-e-commerce-3046

Программа: Менеджер по управлению интернет-магазином
Номер программы Менеджер по управлению интернет-магазином: 3048
Cсылка(url) курса Менеджер по управлению интернет-магазином: https://synergyupgrade.ru/product/menedzher-po-upravleniyu-internet-magazinom-3048

Программа: Нейромаркетинг
Номер программы Нейромаркетинг: 3071
Cсылка(url) курса Нейромаркетинг: https://synergyupgrade.ru/product/nejromarketing-3071

Программа: Графический дизайн с 0 до ПРО
Номер программы Графический дизайн с 0 до ПРО: 677
Cсылка(url) курса Графический дизайн с 0 до ПРО: https://synergyupgrade.ru/product/graficheskij-dizajn-s-0-do-pro-677

Программа: Основы программы Figma
Номер программы Основы программы Figma: 3019
Cсылка(url) курса Основы программы Figma: https://synergyupgrade.ru/product/osnovy-programmy-figma-3019

Программа: Рекламный плакат и знакообразование
Номер программы Рекламный плакат и знакообразование: 3020
Cсылка(url) курса Рекламный плакат и знакообразование: https://synergyupgrade.ru/product/reklamnyj-plakat-i-znakoobrazovanie-3020

Программа: Основы графического дизайна для государственных и муниципальных служащих
Номер программы Основы графического дизайна для государственных и муниципальных служащих: 3028
Cсылка(url) курса Основы графического дизайна для государственных и муниципальных служащих: https://synergyupgrade.ru/product/osnovy-graficheskogo-dizajna-dlya-gosudarstvennyh-i-municipalnyh-sluzhashih-3028

Программа: Профессия: дизайнер интерьера
Номер программы Профессия: дизайнер интерьера: 3035
Cсылка(url) курса Профессия: дизайнер интерьера: https://synergyupgrade.ru/product/professiya-dizajner-interera-3035

Программа: Adobe Photoshop
Номер программы Adobe Photoshop: 3090
Cсылка(url) курса Adobe Photoshop: https://synergyupgrade.ru/product/adobe-photoshop-3090


'''


# GET https://api.proxyapi.ru/proxyapi/balance
#
# Функция создания индексной базы знаний
def create_index_db():
    source_chunks = []
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1024, chunk_overlap=0)

    for chunk in splitter.split_text(database):
        source_chunks.append(Document(page_content=chunk, metadata={}))

    # Initializing the embedding model
    embeddings = OpenAIEmbeddings()

    # Create an index db from separated text fragments
    db = FAISS.from_documents(source_chunks, embeddings)
    return db


db = create_index_db()
#
function_descriptions = [
    {
        "name": "get_dish",
        "description": "Get information about the dish, restaurant name, name of the dish, price of the dish and "
                       "description of the dish",
        "parameters": {
            "type": "object",
            "properties": {
                "restaurant_name": {
                    "type": "string",
                    "description": "The Restaurant name, e.g. Allo BEIRUT",
                },
                "dish_name": {
                    "type": "string",
                    "description": "The dish, name, e.g. Juice Cocktail",
                },
                "dish_description": {
                    "type": "string",
                    "description": "The description of the dish, e.g. Guava, banana, strawberry, mango & milk",
                },
                "dish_price": {
                    "type": "integer",
                    "description": "The dish price, e.g. 120",
                },
                "placed_order": {
                    "type": "string",
                    "description": "The client placed an order, e.g. YES or NO",
                },

            },
            "required": ["restaurant_name", "dish_name", "dish_price", "placed_order"],
        },
    },
]


#
#
# # Запрос в ChatGPT с использованием функций
def answer_function(topic, system=system, index_db=db, temp=0.2):
    # Поиск релевантных отрезков из базы знаний
    docs = index_db.similarity_search(topic, k=5)

    message_content = re.sub(r'\n{2}', ' ', '\n '.join(
        [f'\n#### Document excerpt №{i + 1}####\n' + doc.page_content + '\n' for i, doc in enumerate(docs)]))

    messages = [
        {"role": "system", "content": system},
        {"role": "user",
         "content": f"Here is the document with information to respond to the client: {message_content}\n\n Here is the client's question: \n{topic}"}
    ]

    from openai import OpenAI

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
        temperature=temp,
        max_tokens=1000
        # functions=function_descriptions,  # Add function calling
        # function_call="auto"  # specify the function call
    )

    # completion = openai.ChatCompletion.create(
    #     model=LL_MODEL,
    #     messages=messages,
    #     temperature=temp,
    #     functions=function_descriptions,  # Add function calling
    #     function_call="auto"  # specify the function call
    # )

    # print(f'1st call: finish_reason={completion.choices[0].finish_reason}')
    answer = completion.choices[0].message.content

    # if completion.choices[0].finish_reason == "function_call":
    #     function_answer = completion.choices[0].message
    #     print(f'Сработала функция {function_answer.function_call.name} - нужно извлекать значения параметров функции')
    #     # Извлекаем параметры функции
    #     params = json.loads(function_answer.function_call.arguments)
    #     print(f'params={params}')
    #     # Используем вывод LLM для ручного вызова функции.
    #     function_name = function_answer.function_call.name
    #     chosen_function = eval(function_name)
    #     functionResult = chosen_function(**params)
    #     print(functionResult)
    #     answer, completion = answer_2(topic, message_content, function_answer, functionResult)
    # else:
    #     print(f'Функции не было')

    return answer, completion  # возвращает ответ


#
# # Второй вызов ChatGPT для обработки результатов выполнения функции
# def answer_2(topic, message_content, function_answer, functionResult, system=system, index_db=db, temp=0.2):
#     messages = [
#         {"role": "system", "content": system},
#         {"role": "user",
#          "content": f"Here is the document with information to respond to the client: {message_content}\n\n Here is the client's question: \n{topic}"},
#         {"role": "function", "name": function_answer.function_call.name, "content": functionResult}
#     ]
#
#     completion = openai.ChatCompletion.create(
#         model=LL_MODEL,
#         messages=messages,
#         temperature=temp,
#         functions=function_descriptions,  # Add function calling
#         function_call="none"  # specify the function call
#     )
#     print(f'2st call: finish_reason={completion.choices[0].finish_reason}')
#     answer = completion.choices[0].message.content
#     return answer, completion
#
#
# USER_NAME = "ElonMask"
# USER_ID = "000001"
#
#
# def get_dish(restaurant_name, dish_name, dish_price, dish_description='', placed_order='NO'):
#     """Get information about the dish, restaurant name, name of the dish, price of the dish and description of the
#     dish"""
#     print(f'placed_order={placed_order}')
#     # Output
#     get_dish_info = {
#         "user_name": USER_NAME,
#         "user_id": USER_ID,
#         "restaurant_name": restaurant_name,
#         "dish_name": dish_name,
#         "dish_price": dish_price,
#         "dish_description": dish_description
#     }
#     dish = json.dumps(get_dish_info)
#     if placed_order == 'YES':
#         # Get the current date and time
#         current_datetime = datetime.now(tz=timezone(timedelta(hours=3)))
#         # Format the date and time as a string
#         formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
#         orderfilename = formatted_datetime + "_" + USER_ID + "_order.txt"
#         with open(orderfilename, 'w', encoding='utf-8') as file:
#             file.write(dish)
#
#     return dish
#
#
# # params = {'restaurant_name': 'Allo BEIRUT', 'dish_name': 'Machbous Lamb', 'dish_price': 59, 'dish_description': ''}
# # function_name = 'get_dish'
# # chosen_function = eval(function_name)
# # functionResult = chosen_function(**params)
# # functionResult
#
# topic = 'маркетинг'
st.write("### SYNERGY UPDATE")
# system = st.text_input("Системный промт", '')
system = st.text_area(
    "Системный промт",
    '''Вы являетесь администратором образовательного маркетплейса Synergy Upgrade и отвечаете на вопросы клиентов в чате. Никогда не спешите с ответом,
внимательно прочитайте условия вопроса и дайте точный ответ, ориентируясь на ключевые слова в запросе, учитывая, что текущий уровень знаний клиента: ''' + 'Новичок' + ''',
а особые пожелания клиента: ''' + '' + '''.
Используйте данные только из переданного документа, не используйте данные от себя.
У вас есть документ с информацией обо всех образовательных программах маркетплейса Synergy Upgrade ресторанах, номерах программ, ссылках и описании.
Не упоминайте документ или его фрагменты при ответе, клиенту не обязательно что-либо знать о
документе, который вы используете для подготовки ответа.
В ответе указывай до 5 программ и используй только формат: 
"Номер программы; Твой комментарий о программе; html cсылка на курс" через запятую.

Пример ответа:
    Наименование программы: Интернет-маркетинг,<br/>
    Номер программы:"17", <br/>
    комментарий:"Твой комментарий о программе", <br/>
    Ссылка: <a href="Ссылка">Интернет-маркетинг</a><br/>
    <br/>
    Наименование программы: SMM-маркетинг,<br/>
    Номер программы: "19", <br/>
    комментарий:"Твой комментарий о программе 2", <br/>
    Ссылка:<a href="Ссылка">SMM-маркетинг</a><br/>
    <br/>
    Наименование программы: SMM-маркетинг,<br/>
    Номер программы: "20", <br/>
    комментарий:"Твой комментарий о программе 2", <br/>
    Ссылка:<a href="Ссылка">SMM-маркетинг</a><br/>
    <br/>
    Наименование программы: SMM-маркетинг,<br/>
    Номер программы: "203", <br/>
    комментарий:"Твой комментарий о программе 2", <br/>
    Ссылка:<a href="Ссылка">SMM-маркетинг</a><br/>
    <br/>
    Наименование программы: SMM-маркетинг,<br/>
    Номер программы: "195", <br/>
    комментарий:"Твой комментарий о программе 2", <br/>
    Ссылка:<a href="Ссылка">SMM-маркетинг</a><br/>

 
Отвечайте на все вопросы только на русском языке''',
    height=300
)

# st.write(f"You wrote {len(txt)} characters.")
query = st.text_input("Введите запрос", '')

answer = ''
if query:
    answer, completion = answer_function(topic=query, system=system)  # получите ответ модели

# print(answer)

# topic = 'Хорошо, заказываю'
# answer, completion = answer_function(topic=topic)  # получите ответ модели
# print(answer)

st.write("### Ответ")
# st.code(f"{answer}!", language='python')
st.markdown(f"{answer}", unsafe_allow_html=True)
# st.write(f"{answer}!")

# [
#     {
#     "Номер программы":"17",
#     "комментарий":"Твой комментарий о программе",
#     "Ссылка":"Ссылка на курс"
#     },
#     {
#     "Номер программы":"19",
#     "комментарий":"Твой комментарий о программе 2",
#     "Ссылка":"Ссылка на курс 2"
#     },
#  ]
