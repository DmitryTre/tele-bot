# /client_api/main.py

from pyrogram import Client

api_id = 23529146
api_hash = 'f5476142b28db9137362d39ebcb7d8b1'

# Создаём программный клиент, передаём в него
# имя сессии и данные для аутентификации в Client API
app = Client('my_account', api_id, api_hash)

app.start()
# Отправляем сообщение
# Первый параметр — это id чата (тип int) или имя получателя (тип str).
# Зарезервированное слово 'me' означает собственный аккаунт отправителя.
app.send_message(57190852, 'Привет, это я!')
app.stop()

https://api.telegram.org/bot<ваш-токен>/sendMessage?chat_id=<id_чата_получателя>&text=<текст_сообщения>