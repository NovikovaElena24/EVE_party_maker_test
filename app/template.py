import streamlit as st
from streamlit_javascript import st_javascript
import json
import requests

st.set_page_config(page_title="Календарь мероприятий", layout="centered", initial_sidebar_state="collapsed")
st.title("Календарь мероприятий")

# 🧠 Получаем initData как сериализованный JSON
init_data_raw = st_javascript(
    """
    () => {
        try {
            const tg = window.Telegram?.WebApp;
            if (!tg) return JSON.stringify({ error: "NO_TG_OBJECT" });
            tg.ready();
            tg.expand();
            return JSON.stringify({
                initData: tg.initData || "EMPTY_INIT_DATA",
                platform: tg.platform,
                isExpanded: tg.isExpanded,
                colorScheme: tg.colorScheme
            });
        } catch (e) {
            return JSON.stringify({ error: "JS_ERROR", message: e.message });
        }
    }
    """
)

# 🔍 Отладка
st.subheader("init_data_raw:")
st.write(init_data_raw)

# 🧪 Парсим JSON
try:
    init_data = json.loads(init_data_raw)
except Exception as e:
    st.error(f"Ошибка парсинга initData: {e}")
    init_data = {}

# ⬇️ Отображаем разобранный словарь
st.subheader("Parsed initData")
st.json(init_data)

# 🔒 Проверка подписи, если initData валиден
if isinstance(init_data, dict) and init_data.get("initData") not in ["", "EMPTY_INIT_DATA"]:
    response = requests.post("https://87da-37-150-246-43.ngrok-free.app/verify", json={"initData": init_data["initData"]})
    result = response.json()
    if result.get("ok"):
        user = result.get("user", {})
        st.success(f"Вы авторизованы как {user.get('username', 'гость')} (ID: {user.get('id')})")
    else:
        st.warning("Проверка подписи не удалась")
else:
    st.warning("Нет initData от Telegram WebApp")


# import streamlit as st
# from streamlit_calendar import calendar
# from datetime import datetime, timezone, timedelta
# # from database.requests import add_meeting  # Импортируйте вашу функцию здесь
# import asyncio
# from streamlit_javascript import st_javascript
# import json
# import requests
# import time
# import streamlit.components.v1 as components



# # Заголовок страницы
# st.set_page_config(page_title="Календарь", layout="centered", initial_sidebar_state="collapsed")
# # st.set_page_config(page_title="Календарь мероприятий", layout="centered")
# # st.title("Календарь мероприятий в Telegram")


# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# # components.html(
# #     """
# #     <script src="https://telegram.org/js/telegram-web-app.js?57"></script>
# #     """,
# #     height=0,
# # )

# # Получаем initData из Telegram WebApp
# # init_data = st_javascript(
# #     """
# #     () => {
# #         const tg = window.Telegram.WebApp;
# #         tg.expand();
# #         return tg.initData || "";
# #     }
# #     """
# # )
# # init_data = st_javascript(
# #     """
# #     () => {
# #         const tg = window.Telegram.WebApp;
# #         tg.expand();
# #         console.log("initData:", tg.initData);
# #         console.log("initDataUnsafe:", tg.initDataUnsafe);
# #         return tg.initData || tg.initDataUnsafe || "";
# #     }
# #     """
# # )

# # init_data = st_javascript(
# #     """
# #     () => {
# #         const tg = window.Telegram?.WebApp;
# #         if (!tg) {
# #             return "tg_undefined";
# #         }
# #         if (!tg.initData) {
# #             return "initData_empty";
# #         }
# #         return tg.initData;
# #     }
# #     """
# # )

# # init_data = st_javascript(
# #     """
# #     () => {
# #         try {
# #             const tg = window.Telegram?.WebApp;
# #             if (!tg) {
# #                 return "Telegram WebApp is undefined";
# #             }
# #             if (!tg.initData) {
# #                 return "initData is missing or empty";
# #             }
# #             return tg.initData;
# #         } catch (e) {
# #             return "JS Error: " + e.toString();
# #         }
# #     }
# #     """
# # )

# # init_data = st_javascript(
# #     """
# #     () => {
# #         try {
# #             const tg = window.Telegram.WebApp;
# #             tg.ready();
# #             tg.expand();
# #             return tg.initData || "empty";
# #         } catch (e) {
# #             return "tg_error: " + e.message;
# #         }
# #     }
# #     """
# # )

# # init_data = st_javascript(
# #     """
# #     () => {
# #         try {
# #             const tg = window.Telegram.WebApp;
# #             tg.ready();
# #             tg.expand();
# #             console.log("Telegram WebApp initialized", tg.initData);
# #             return {
# #                 initData: tg.initData || "empty",
# #                 isExpanded: tg.isExpanded,
# #                 platform: tg.platform,
# #                 colorScheme: tg.colorScheme
# #             };
# #         } catch (e) {
# #             console.error("Error initializing Telegram WebApp:", e);
# #             return "tg_error: " + e.message;
# #         }
# #     }
# #     """
# # )

# init_data = st_javascript(
#     """
#     (() => {
#         const tgScript = document.createElement("script");
#         tgScript.src = "https://telegram.org/js/telegram-web-app.js";
#         document.head.appendChild(tgScript);

#         tgScript.onload = () => {
#             const tg = window.Telegram.WebApp;
#             tg.ready();
#             tg.expand();
#             return {
#                 initData: tg.initData || "empty",
#                 isExpanded: tg.isExpanded,
#                 platform: tg.platform,
#                 colorScheme: tg.colorScheme
#             };
#         };

#         tgScript.onerror = () => {
#             console.error("Failed to load Telegram Web App script.");
#         };
#     })();
#     """
# )

# # time.sleep(3)
# st.write("Telegram WebApp info:", str(init_data))



# # # Значения по умолчанию
# # username = "гость"
# # user_id = "аноним"

# # st.write("init_data:", init_data)

# # Проверка подписи Telegram через бекенд
# if init_data:
#     try:
#         # verify_url = "http://localhost:8000/verify"
#         verify_url = "https://87da-37-150-246-43.ngrok-free.app/verify"
#         response = requests.post(verify_url, json={"initData": init_data})
#         result = response.json()
#         if result.get("ok"):
#             user_data = result.get("user", {})
#             username = user_data.get("username", "гость")
#             user_id = str(user_data.get("id", "аноним"))
#             st.success(f"Вы авторизованы как {username}")
#         else:
#             st.warning("Не удалось проверить Telegram-подпись.")
#     except Exception as e:
#         st.error(f"Ошибка при верификации: {e}")
# else:
#     st.warning("Не удалось получить initData из Telegram WebApp.")


# calendar_options = {
#     "editable": True,
#     "selectable": True,
#     "headerToolbar": {
#         "left": "today prev,next",
#         "center": "title",
#         "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
#     },
#     # "slotDuration": "00:30:00",
#     "slotMinTime": "00:00:00",
#     "slotMaxTime": "24:00:00",
#     "timeZone": "UTC",  # Устанавливаем временную зону UTC
#     "slotLabelFormat": {  # Устанавливаем формат отображения времени
#         "hour": "2-digit",
#         "minute": "2-digit",
#         "hour12": False,  # Отключаем 12-часовой формат
#     },
#     # "initialView": "resourceTimelineDay",
#     "initialView": "timeGridWeek",  # Устанавливаем режим timeGrid
#     # "resourceGroupField": "building",
#     # "resources": [
#     #     {"id": "a", "building": "Building A", "title": "Building A"},
#     #     {"id": "b", "building": "Building A", "title": "Building B"},
#     #     {"id": "c", "building": "Building B", "title": "Building C"},
#     #     {"id": "d", "building": "Building B", "title": "Building D"},
#     #     {"id": "e", "building": "Building C", "title": "Building E"},
#     #     {"id": "f", "building": "Building C", "title": "Building F"},
#     # ],
# }
# # calendar_events = [
# #     {
# #         "title": "Event 1",
# #         "start": "2023-07-31T08:30:00",
# #         "end": "2023-07-31T10:30:00",
# #         "resourceId": "a",
# #     },
# #     {
# #         "title": "Event 2",
# #         "start": "2023-07-31T07:30:00",
# #         "end": "2023-07-31T10:30:00",
# #         "resourceId": "b",
# #     },
# #     {
# #         "title": "Event 3",
# #         "start": "2023-07-31T10:40:00",
# #         "end": "2023-07-31T12:30:00",
# #         "resourceId": "a",
# #     }
# # ]
# custom_css = """
#     .fc-event-past {
#         opacity: 0.8;
#     }
#     .fc-event-time {
#         font-style: italic;
#     }
#     .fc-event-title {
#         font-weight: 700;
#     }
#     .fc-toolbar-title {
#         font-size: 2rem;
#     }
# """

# calendar = calendar(
#     # events=calendar_events,
#     options=calendar_options,
#     custom_css=custom_css,
#     key="calendar",  # Assign a widget key to prevent state loss
# )
# st.info("Выберите мероприятие и нажмите 'Записаться'")
# # st.write(calendar)

# # Инициализация session_state
# if "selected_range" not in st.session_state:
#     st.session_state.selected_range = None

# # Обработка выбора времени
# if calendar:
#     callback_data = calendar.get("callback")

#     if callback_data:
#         if callback_data == "select":
#             # Обработка диапазона времени
#             st.session_state.selected_range = {
#                 # "start": calendar["select"]["start"],
#                 # "end": calendar["select"]["end"],
#                 "start": (datetime.fromisoformat(calendar["select"]["start"])).isoformat(),
#                 "end": (datetime.fromisoformat(calendar["select"]["end"])).isoformat(),
#             }
#         elif callback_data == "dateClick":
#             # Обработка одного выбранного времени
#             st.session_state.selected_range = {
#                 # "start": calendar["dateClick"]["date"],
#                 # "end": calendar["dateClick"][
#                 #     "date"
#                 # ],  # Устанавливаем конец на то же время
#                 "start": (datetime.fromisoformat(calendar["dateClick"]["date"])).isoformat(),
#                 "end": (datetime.fromisoformat(calendar["dateClick"]["date"]) + timedelta(minutes=30)).isoformat(),
#             }


# # Отправка записи на API
# if calendar and "start" in calendar:
#     start_time = st.session_state.selected_range["start"]
#     end_time = st.session_state.selected_range["end"]

#     date = datetime.fromisoformat(start_time).date()
#     start_time_obj = datetime.fromisoformat(start_time).time()
#     end_time_obj = datetime.fromisoformat(end_time).time()

#     # title = calendar.get("title", "Без названия")
#     # time = calendar["start"]

#     st.success(f"Вы выбрали: {date} в {start_time_obj}-{end_time_obj}")

#     if st.button("Записаться"):
#         try:
#             # register_url = "http://localhost:8000/register"
#             register_url = "https://87da-37-150-246-43.ngrok-free.app/register"
#             payload = {
#                 "date": date,
#                 "start_time": start_time_obj,
#                 "end_time": end_time_obj,
#                 "tg_id": user_id,
#             }
#             reg_response = requests.post(register_url, json=payload)
#             reg_result = reg_response.json()

#             if reg_response.status_code == 200:
#                 st.success("Вы успешно записались!")
#             else:
#                 st.error(f"Ошибка: {reg_result.get('detail', 'Неизвестная ошибка')}")
#         except Exception as e:
#             st.error(f"Ошибка при обращении к API: {e}")
















# # # # # Кнопка "Записаться"
# # # # if st.session_state.selected_range:
# # # #     start_time = st.session_state.selected_range["start"]
# # # #     end_time = st.session_state.selected_range["end"]

# # # #     st.write("Выбранный диапазон (UTC):")
# # # #     st.write("Начало:", start_time)
# # # #     st.write("Окончание:", end_time)

# # # #     if st.button("Записаться"):
# # # #         st.success("Запись успешна! Начало: {}, Окончание: {}".format(start_time, end_time))
# # # # else:
# # # #     # st.write(calendar.get("callback"))
# # # #     # st.write(st.session_state.selected_range)
# # # #     st.warning("Пожалуйста, выберите диапазон времени для записи.")


# # # Кнопка "Записаться"
# # if st.session_state.selected_range:
# #     start_time = st.session_state.selected_range["start"]
# #     end_time = st.session_state.selected_range["end"]

# #     date = datetime.fromisoformat(start_time).date()
# #     start_time_obj = datetime.fromisoformat(start_time).time()
# #     end_time_obj = datetime.fromisoformat(end_time).time()

# #     st.write("Выбранный диапазон (UTC):")
# #     st.write("Начало:", start_time)
# #     st.write("Окончание:", end_time)


# #     # tg_id = 858747013  # Здесь вы можете получить tg_id пользователя

# #     if st.button("Записаться"):
# #         try:
# #             register_url = "http://localhost:8000/register"
#             # register_url = "https://87da-37-150-246-43.ngrok-free.app/register"
# #             payload = {
# #                 "date": date,
# #                 "start_time": start_time,
# #                 "end_time": end_time,
# #                 "tg_id": user_id
# #             }
# #             resp = requests.post(register_url, json=payload)
# #             result = resp.json()
# #             if result.get("ok"):
# #                 st.success("Вы успешно записались!")
# #             else:
# #                 st.error(f"Ошибка: {result.get('error')}")
# #         except Exception as e:
# #             st.error(f"Ошибка при запросе: {e}")

# #     # if st.button("Записаться"):
# #     #     async def save_meeting():
# #     #         # Преобразование времени в нужный формат
# #     #         date = datetime.fromisoformat(start_time).date()
# #     #         start_time_obj = datetime.fromisoformat(start_time).time()
# #     #         end_time_obj = datetime.fromisoformat(end_time).time()

# #     #         # Вызов функции для добавления встречи
# #     #         await add_meeting(date, start_time_obj, end_time_obj, tg_id)
# #     #         st.success("Запись успешна!")

# #     #     # Запуск асинхронной функции
# #     #     asyncio.run(save_meeting())


# # # # async def save_meeting():
# # # #     date = datetime.fromisoformat(start_time).date()
# # # #     start_time_obj = datetime.fromisoformat(start_time).time()
# # # #     end_time_obj = datetime.fromisoformat(end_time).time()
# # # #     await add_meeting(date, start_time_obj, end_time_obj, tg_id)
# # # #     st.session_state['meeting_saved'] = True

# # # # def run_async_task():
# # # #     try:
# # # #         loop = asyncio.get_running_loop()
# # # #     except RuntimeError:
# # # #         loop = asyncio.new_event_loop()
# # # #         asyncio.set_event_loop(loop)
# # # #         loop.run_until_complete(save_meeting())
# # # #     else:
# # # #         asyncio.run_coroutine_threadsafe(save_meeting(), loop)

# # # # if st.button("Записаться"):
# # # #     st.session_state['meeting_saved'] = False
# # # #     run_async_task()

# # # # if st.session_state.get('meeting_saved'):
# # # #     st.success("Запись успешна!")


# # # async def save_meeting():
# # #     # Преобразование времени в нужный формат
# # #     date = datetime.fromisoformat(start_time).date()
# # #     start_time_obj = datetime.fromisoformat(start_time).time()
# # #     end_time_obj = datetime.fromisoformat(end_time).time()

# # #     # Вызов функции для добавления встречи
# # #     await add_meeting(date, start_time_obj, end_time_obj, tg_id)
# # #     st.success("Запись успешна!")

# # # if st.button("Записаться"):
# # #     # await save_meeting()  # Просто вызываем функцию с await
# # #     asyncio.run(save_meeting())

# # # # # Запуск асинхронной функции
# # # # if st.button("Записаться"):
# # # #     # asyncio.run(save_meeting())  # Если это в основном коде
# # # #     # Создаем задачу и выполняем ее
# # # #     task = asyncio.create_task(save_meeting())
# # # #     # # Используем текущий цикл событий
# # # #     # loop = asyncio.get_event_loop()
# # # #     # if loop.is_running():
# # # #     #     # Если цикл уже запущен, используем create_task
# # # #     #     asyncio.create_task(save_meeting(start_time, end_time, tg_id))
# # # #     # else:
# # # #     #     # Если цикл не запущен, запускаем его
# # # #     #     loop.run_until_complete(save_meeting(start_time, end_time, tg_id))

# # # # if st.button("Записаться"):
# # # #     loop = asyncio.get_event_loop()
# # # #     loop.run_until_complete(save_meeting())

# # # # # Функция для запуска асинхронного кода
# # # # def run_async_task():
# # # #     loop = asyncio.get_event_loop()
# # # #     loop.create_task(save_meeting())

# # # # run_async_task()

# # # # streamlit run template.py