with open('./db_sales.csv', 'w') as f:
    f.write('id,sales\n')
    f.close()

with open('./db_restock.csv', 'w') as f:
    f.write('id,restocks\n')
    f.close()

with open('./db_users.csv', 'w') as f:
    f.write('id,email,paid\n')
    f.close()
     