import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glasgowgems.settings')
				
import django
django.setup()
from gems.models import Category, Gem, Comment

def populate():

	education_related_gems = [
		{"name":"Boyd Orr Building",
		"address":"120 University Avenue, Glasgow, G12 8QR",
		"description":"Sample description of ",
		"image":"gems_images/boyd_orr.jpg",
		"image_source":"www.gla.ac.uk",
		"latitude": 55.873560,  "longitude": -4.292713,
		"likes":10,
		"reported":False,
		},
		
		{"name":"Gilbert Scott Building",
		"address":"University Avenue, Glasgow, G12 8QQ",
		"description":"Sample description of ",
		"image":"gems_images/gilbert_scott.jpg",
		"image_source":"www.glasgowguardian.co.uk",
		"latitude": 55.871457,  "longitude": -4.288542,
		"likes":20,
		"reported":False,
		}
	]
		
	sports_related_gems = [
		{"name":"Celtic Park",
		"address":"The Celtic Way, Glasgow, G40 3RE",
		"description":"Sample description of ",
		"image":"gems_images/celtic_park.jpg",
		"image_source":"www.footballtripper.com",
		"latitude": 55.849758,  "longitude": -4.205469,
		"likes":10,
		"reported":True,
		},

		{"name":"Hampden Park",
		"address":"Letherby Drive, Glasgow, G42 9BA",
		"description":"Sample description of ",
		"image":"gems_images/hampden_park.jpg",
		"image_source":"www.footballtripper.com",
		"latitude": 55.825839,  "longitude": -4.251974,
		"likes":10,
		"reported":True,
		},

		{"name":"Ibrox Stadium",
		"address":"150 Edmiston Dr, Glasgow, G51 2XD",
		"description":"Sample description of ",
		"image":"gems_images/ibrox_stadium.jpg",
		"image_source":"www.footballtripper.com",
		"latitude": 55.853226,  "longitude": -4.309215,
		"likes":10,
		"reported":True,
		}
	]
	
	open_spaces_gems = [
		{"name":"Kelvingrove Park",
		"address":"Kelvingrove Park, Glasgow, G3 7SD",
		"description":"Sample description of ",
		"image":"gems_images/kelvingrove_park.jpg",
		"image_source":"www.drookitagain.co.uk",
		"latitude": 55.869476,  "longitude": -4.284280,
		"likes":18,
		"reported":False,
		}
	]
	
	religion_related_gems = [
		{"name":"Glasgow Necropolis",
		"address":"Wishart St, Glasgow, G4 0UY",
		"description":"Sample description of  ",
		"image":"gems_images/glasgow_necropolis.jpg",
		"image_source":"www.atlasobscura.com",
		"latitude": 55.862713,  "longitude": -4.230764,
		"likes":18,
		"reported":False,
		}
	]
	
	cats = {"Bridges": {"description": "Any bridges."},
			"Castles": {"description": "Any castles."},
			"Education related": {"gems": education_related_gems,
								  "description": "Any education related architecture."},
			"Fountains": {"description": "Any fountains."},
			"Hotels": {"description": "Any hotels."},
			"Houses": {"description": "Any houses."},
			"Industrial": {"description": "Any industrial architecture."},
			"Leisure related": {"description": "Any leisure related architecture."},
			"Manor houses": {"description": "Any manor houses."},
			"Modern": {"description": "Any modern architecture."},
			"Monuments": {"description": "Any monuments."},
			"Municipal": {"description": "Any municipal architecture."},
			"Museums and Galleries": {"description": "Any museums and galleries."},
			"Music venues": {"description": "Any music venues."},
			"Open spaces": {"gems": open_spaces_gems,
							"description": "Any open space 'architecture'."},
			"Other": {"description": "Any other architecture."},
			"Religion related": {"gems": religion_related_gems,
								 "description": "Any religion related architecture."},
			"Sculptures": {"description": "Any sculptures."},
			"Sports related": {"gems": sports_related_gems,
							   "description": "Any sports related architecture."},
			"Tenements": {"description": "Any tenements."},
			"Theatres": {"description": "Any theatres."},
			"Transport related": {"description": "Any transport related architecture."},
			}
	
	for cat, cat_data in cats.items():
		c = add_cat(cat, cat_data["description"])
		for g in cat_data.get("gems", []):
			added_g = add_gem(c, g["name"], g["address"], g["description"] + g["name"],
							  g["image"], g["image_source"], g["latitude"], g["longitude"],
							  g["likes"], g["reported"])
			add_com(added_g, "This is a sample comment for " + g["name"] + ".")
			
	# Print out the categories, gems and comments we have added.
	for c in Category.objects.all():
		for g in Gem.objects.filter(category=c):
			for com in Comment.objects.filter(gem=g):
				print("- {0} - {1} - {2}".format(str(c), str(g), str(com)))
	
def add_gem(cat, name, address, description, image, image_source,
			latitude, longitude, likes, reported):
		g = Gem.objects.get_or_create(category=cat, name=name)[0]
		g.address=address
		g.description=description
		g.image=image
		g.image_source=image_source
		g.latitude=latitude
		g.longitude=longitude
		g.likes=likes
		g.reported=reported
		g.save()
		return g
	
def add_cat(name, description):
		c = Category.objects.get_or_create(name=name)[0]
		c.description=description
		c.save()
		return c

def add_com(gem, text):
	com = Comment.objects.get_or_create(gem=gem)[0]
	com.text=text
	com.save()
	return com
	
if __name__ == '__main__':
	print("Starting Glasgow Gems population script...")
	populate()
