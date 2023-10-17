from database import db_helper

f_db = db_helper.db('test.db')

f_db.add_row('users',{db_helper.k_user_id: 235,db_helper.k_login: 'somelogin'})
