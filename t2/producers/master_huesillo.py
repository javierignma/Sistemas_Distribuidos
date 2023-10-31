import producers as prod
import random
import time
import sys

if len(sys.argv) > 3:
    print("Usage: python3 master_huesillero.py <ID> <isPaid (0=false and 1=True)>")
    exit()

ID = sys.argv[1]
isPaid = int(sys.argv[2])

prod.send_registration(ID, isPaid)

stock = 5

while True:
    waiting_time = random.randint(3, 5)
    time.sleep(waiting_time)
    if stock == 0:
        prod.send_no_stock(ID)
        stock = 5
    prod.send_sale(ID)
    stock -= 1