from models import *

barbershops = [
    {'name' : 'Vagabond Hair Studio', 'address' : 'Bloc G1, Bulevardul Unirii 65, Bucuresti', 'rating' : 4.7, 'ratings_recv' : 58, 'coordX' : 44.426309, 'coordY' : 26.123891},
    {'name' : 'Office 21 Barbershop', 'address' : 'Strada Inginer Cristian Pascal 34, Bucuresti', 'rating' : 4.2, 'ratings_recv' : 126, 'coordX' : 44.450964, 'coordY' : 26.054762},
    {'name' : 'CREATIVE BARBER', 'address' : 'Bulevardul Carol I 46, Bucuresti', 'rating' : 4.4, 'ratings_recv' : 82, 'coordX' : 44.437675, 'coordY' : 26.111021}
]

barbers = [
    {'name' : 'Ionutz', 'rating' : 4.9, 'ratings_recv' : 20, 'bbs_id' : 1},
    {'name' : 'Mihai', 'rating' : 4.7, 'ratings_recv' : 19, 'bbs_id' : 1},
    {'name' : 'Gabi', 'rating' : 4.5, 'ratings_recv' : 19, 'bbs_id' : 1},
    {'name' : 'Mihai', 'rating' : 4.2, 'ratings_recv' : 42, 'bbs_id' : 2},
    {'name' : 'Daniel', 'rating' : 4.0, 'ratings_recv' : 42, 'bbs_id' : 2},
    {'name' : 'Jorge', 'rating' : 4.4, 'ratings_recv' : 42, 'bbs_id' : 2},
    {'name' : 'Dragos', 'rating' : 4.5, 'ratings_recv' : 14, 'bbs_id' : 3},
    {'name' : 'Vlad', 'rating' : 4.4, 'ratings_recv' : 14, 'bbs_id' : 3},
    {'name' : 'Cristi', 'rating' : 4.3, 'ratings_recv' : 14, 'bbs_id' : 3}
]

services = [
    {'name' : 'Tuns modern', 'price' : 50, 'bbs_id' : 1},
    {'name' : 'Tuns modern + spalat', 'price' : 65, 'bbs_id' : 1},
    {'name' : 'Aranjat barba', 'price' : 25, 'bbs_id' : 1},
    {'name' : 'Tuns cu ciobul', 'price' : 20, 'bbs_id' : 2},
    {'name' : 'Tuns zero', 'price' : 10, 'bbs_id' : 2},
    {'name' : 'Aranjat barba', 'price' : 15, 'bbs_id' : 2},
    {'name' : 'Lumberjack-Hair And Beard', 'price' : 80, 'bbs_id' : 3},
    {'name' : 'Tuns', 'price' : 60, 'bbs_id' : 3},
    {'name' : 'Aranjat barba', 'price' : 30, 'bbs_id' : 3}
]

def init_db_data():
    for bbs_json in barbershops:
        bbs = BarbershopModel(bbs_json)
        bbs.save_to_db()

    for b_json in barbers:
        b = BarberModel(b_json)
        b.save_to_db()

    for s_json in services:
        s = ServiceModel(s_json)
        s.save_to_db()
