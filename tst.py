from workers.workers import Query

query = Query()

print(query.query_messages(host_id='achira'))
print(query.query_user('achira'))