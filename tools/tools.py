import json
import os

from aiogram.types import Message, User


k_data = 'data/'
k_users_files = 'users_files/'
k_users_dir = 'users/'


s_dir_list = [k_data,k_users_files,k_data + k_users_dir]
def makedir(f_path):
        if not os.path.exists(f_path):
                path = os.path.join(f_path)
                os.mkdir(path)
for q_path in s_dir_list:
        makedir(q_path)

#utf-8 cp1251
def get_data(f_id):
  try:
    f = open(k_data+f_id, 'r',encoding='utf-8')
  except FileNotFoundError as e:
    #print('no data yet')
    return 404
  fData = False
  try:
    fData = json.load(f)
  except ValueError as e:
    #print('chat data still empty')
    return 404
  m_chat = fData
  #print(f'load data')
  f.close()
  return m_chat


def set_data(f_path, f_param):
  f_path = k_data + f_path
  try:
    f = open(f_path, 'r')
  except FileNotFoundError as e:
    f = open(f_path, 'x')
    f = open(f_path, 'r')
  fData = False
  try:
    fData = json.load(f)
  except ValueError as e:
    pass
    #print('chat data still empty')
  f.close()

  fData = json.dumps(f_param,ensure_ascii=False)
  with open(f_path, "w",encoding='utf-8') as my_file:
    my_file.write(fData)
    my_file.close()
  #print(fData)

class MyCallback():

  message: Message
  from_user: User

  def __init__(self,f_msg: Message):
    self.message = f_msg
    self.from_user = f_msg.from_user

  async def answer(self):
    pass