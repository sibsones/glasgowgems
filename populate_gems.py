import os
import django
from django.template.defaultfilters import slugify

os.environ.setdefault(
					'DJANGO_SETTINGS_MODULE',
					'glasgowgems.settings',)
				
django.setup()
from gems.models import User, Category, Page, Comment					

def populate():

	cat_A_pages = [
		
		{"name":"Boyd Orr"
		'''
		"address":"number, street, post code",
		"description":"",
		"image": None,
		"imageSource":"source",
		"likes": 10,
		"reported":False,
		"addedBy":"user1289",
		"addedOn":"02/03/19",
		"slug":"boyd-orr",
		'''
		},
		
		{"name":"University Main Building"
		'''
		"address":"number, street, post code",
		"description":"",
		"image":None,
		"imageSource":"source",
		"likes":16,
		"reported":False,
		"addedBy":"user8182",
		"addedOn":"02/03/19",
		"slug":"univserity-main-building",
		'''
		},
	]
		
	cat_B_pages = [

		{"name":"Hampden Park"
		'''
		"address":"number, street, post code",
		"description":"",
		"image":None,
		"imageSource":"source",
		"likes":11,
		"reported":False,
		"addedBy":"user7127",
		"addedOn":"02/03/19",
		"slug":"hampden-park",
		'''
		},

		{"name":"Ibrox Stadium"
		'''
		"address":"number, street, post code",
		"description":"",
		"image":None,
		"imageSource":"source",
		"likes":1,
		"reported":False,
		"addedBy":"user1234",
		"addedOn":"02/03/19",
		"slug":"ibrox-stadium",
		'''
		},
	]
	
	
	cat_C_pages = [

		{"name":"Kelvingrove Park"
		'''
		"address":"number, street, post code",
		"description":"",
		"image":None,
		"imageSource":"source",
		"likes":18,
		"reported":False,
		"addedBy":"user7623",
		"addedOn":"02/03/19",
		"slug":"kelvingrove-park",
		'''
		},
		
		{"name":"Glasgow Necropolis"
		'''
		"address":"number, street, post code",
		"description":"",
		"image":None,
		"imageSource":"source",
		"likes":13,
		"reported":False,
		"addedBy":"user9920",
		"addedOn":"02/03/19",
		"slug":"glasgow-necropolis",
		'''
		},
	]	
		
		
	#categories dictionary
	cats = {'cat_A': {'pages': cat_A_pages},
			'cat_B': {'pages': cat_B_pages},
			'cat_C': {'pages': cat_C_pages},
			}
			
	
		
	for cat, cat_data in cats.items():
		c = add_cat(cat)
		for page in cat_data["pages"]:
			add_page(cat)
			
			
	
	def add_page(cat):
		p = Page.objects.get_or_create(category=cat)[0]
		p.address=None
		p.description=None
		p.image=None
		p.imageSource=None
		p.likes=None
		p.reported=None
		p.addedBy=None
		p.addedOn=None
		p.save()
		return p
		
	
	def add_cat(name):
		c = Category.objects.get_or_create(name=name)[0]
		c.save()
		return c
	
		
				
	if __main__ == '__main__':
		print("Starting gems population script...")
		populate()
		
		
		
		
		
		
		
		
		
		
		
		
		