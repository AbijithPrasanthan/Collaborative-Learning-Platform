import urllib, json
import requests

def email_verification(email):
    
	domain_extract = email.split("@")[1] 
	listed = domain_extract.split(".")[::-1]
	domain = ""
 
	for i in range(len(listed)):
		
		temp = ""
		temp = temp + listed[i]
		if i!=0:
			temp = temp + "."
		domain = temp + domain
		 
		try:
			r = requests.get('http://universities.hipolabs.com/search?domain='+domain)
			print(r.json()[0]['domains'])
			return 1
		except:
			pass

	return 0