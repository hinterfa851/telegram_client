import json
import requests
import csv
from telethon.sync import TelegramClient
from datetime import date, datetime
import telethon
import os
from telethon.tl.functions.messages import GetHistoryRequest

api_id = ####
api_hash = ####
app_title = ####
username = ###

token = #####
chat_id = ####
get_updates_url = ####

proxy = ('russia-dd.proxy.digitalresistance.dog', 443, 'ddd41d8cd98f00b204e9800998ecf8427e')

client = TelegramClient(username, api_id, api_hash,
                        connection=telethon.connection.ConnectionTcpMTProxyRandomizedIntermediate,
                        proxy=proxy)

client.start()


async def move_to_shelter(i, writer):
    writer.writerow({'N': i['id'], 'link': i['message']})



async def delete_message(idd):
    entity = await client.get_entity(#####)
    await client.delete_messages(entity, idd)


async def check_messages(all_messages):
    with open("data.csv", 'a') as file:
        fieldnames = ['N', 'link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        n = 0
        for i in all_messages:
            if (i['id'] != 1):
       #         print(i['id'])
                n += 1
    #    print(n)
                if i['message'].find('https://www.avito.ru/') != -1:
                    response = requests.get(i['message'], allow_redirects=False)
                    if response.text.find('Это объявление закрыто владельцем. Оно более не актуально.') != -1:
                        #print(i['id'])
                       await delete_message(i['id'])
                    elif response.text.find('Срок размещения этого объявления истёк') != -1:
                       await move_to_shelter(i, writer)
                       await delete_message(i['id'])
                    elif (response.text.find('Добавить заметку') == -1):
                       # print(i['id'])
                       await delete_message(i['id'])

async def dump_all_messages(channel):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''

        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        await check_messages(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break


def del_row_csv(list_c, reader):
    with open("data_res.csv", 'w') as file1:
        fieldnames = ['N', 'link']
        writer = csv.DictWriter(file1, fieldnames=fieldnames)
        writer.writeheader()
        counter = 0
        for row in reader:
            if (counter in list_c):
                pass
            else:
                writer.writerow({'N': row['id'], 'link': row['message']})
            counter += 1



def check_database(channel):
    with open("data.csv") as file:
        reader = csv.DictReader(file)
        counter = 0
        list_c =[]
        for row in reader:
            response = requests.get(row['link'], allow_redirects=False)
            if response.text.find('Срок размещения этого объявления истёк') == -1:
                  if response.text.find('Добавить заметку') != -1:
                      client.send_message(channel, row['link'])
                  counter += 1
                  list_c.append(counter)
        del_row_csv(list_c, reader)


async def main():
    channel = await client.get_entity(#####)
    await dump_all_messages(channel)
    check_database(channel)
    os.remove('C:\\Users\\My\\PycharmProjects\\parser\\data.csv')
    os.rename('data_res.csv', 'data.csv')
#    await client.send_message(channel, 'test message')
#    client.disconnect()


with client:
    client.loop.run_until_complete(main())
