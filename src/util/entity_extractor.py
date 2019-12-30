import paralleldots
paralleldots.set_api_key("skGC4w3X7XVHQJhzNYbXolP4DyL4CNyhXjPfx4f8lRU")
lang_code = "en"

def group_extractor(text):
	response = paralleldots.ner(text,lang_code)
	#print(response)	
	l = [el['name'] for el in response['entities'] if el['category'] == 'group' or el['category'] == 'place']

	return l
