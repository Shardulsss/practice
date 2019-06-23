import facebook
import sqlite3

# Enter token
token = "Enter_here"

conn = sqlite3.connect("database.db")
cur = conn.cursor()



#creating table with 4 coloumns
cur.execute("""create table if not exists data
			(
				name text,
				ID integer,
				post text,
				like text
			)
					""")

# call GraphAPI with the token
graph = facebook.GraphAPI(access_token=token)

# store the user details in an object
post = graph.get_object(id='me', fields='id,name,posts,likes')



name = post['name']
id = post['id']
p = []
for message in post['posts']['data']:
    try:
        p.append(message['message'])
    except KeyError:
        pass
posts = ', '.join(p)
lp = []
for page in post['likes']['data']:
    lp.append(page['name'])

page = ', '.join(lp)



cur.execute("insert into data values(?, ?, ?, ?)",(name, id, posts, page))
print("Data Pulled :")
cur.execute("SELECT * FROM data ")
print(cur.fetchall())



print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#to find user with specific keyword from his likes 
cur.execute("SELECT * FROM data WHERE like LIKE '%Enter_here%' ")    #edit keyword here
print("Data of user with specified keyword :")
print(cur.fetchall())
conn.commit()


conn.close()