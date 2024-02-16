import json
import requests
import os

cookies = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

if not os.path.exists("output.txt"):
    with open("output.txt", 'w') as file:
        file.write('')
    already_done = []
else:
    already_done = [json.loads(line)['name']+json.loads(line)['address'] for line in open("output.txt", "r").readlines()]

def get_place(x, y, term):
    with open("output.txt", "a") as file:
        response = requests.get(
            'https://www.google.com/maps/search/{}/@{},{},17z/data=!3m1!4b1?hl=en&entry=ttu'.format(term.replace(" ", "+"),x,y),
            cookies=cookies,
            headers=headers,
        )
        response_decoded = response.content.decode()
        json_object = json.loads(response_decoded.split("window.APP_INITIALIZATION_STATE=")[1].split(";window.APP_FLAGS")[0])

        restaurants_object = json.loads(json_object[3][2].split("\n")[1])

        for restaurant in restaurants_object[0][1][1::]:
            try:
                name = restaurant[14][11]
                restaurant_general_info = restaurant[14][4]
                
                try:
                    price_info = restaurant_general_info[2]
                except:
                    price_info = ""

                try:
                    note = restaurant_general_info[7]
                    avis = restaurant_general_info[8]
                except:
                    note = -1
                    avis = -1
                
                address = ", ".join(restaurant[14][2][0:2])

                categories = restaurant[14][13]
                photo_id = restaurant[14][51][0][0][15][0][0][0]

                coords = restaurant[14][9][2::]

                try:
                    horaire = {}
                    for day in restaurant[14][203][0]:
                        
                        if day[3][0][0]!= "Closed":
                            ouverture = "-".join([str(x) for x in day[3][0][1][0]])
                            fermeture = "-".join([str(x) for x in day[3][0][1][1]])
                            horaire[day[0]] = [ouverture, fermeture]
                except:
                    horaire = {}
                
                if not name+address in already_done:
                    already_done.append(name+address)
                    file.write(json.dumps({"name":name, "address":address, "note":note, "avis":avis, "categories":categories, "photo_id":photo_id, "horaire":horaire, "price_info":price_info, "coords":coords})+"\n")
                    print("saved")
            
            except Exception as e:
                import traceback
                traceback.print_exc()

x_depart, y_depart = 37.784552, -122.511545
x_fin,y_fin = 37.716959, -122.365976

terms = [
    "restaurant"
]

pas = 0.002
x = x_depart
y = y_depart
i = 1

while x > x_fin:
	y = y_depart
	while y < y_fin:
		try:
			place = get_place(str(x),str(y), "restaurant")
		except Exception as e:
			print(e)
		i+=1
		y+=pas
	x-=pas