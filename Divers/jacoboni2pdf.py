# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import os
import sys

os.system("clear")
print "Bienvenue dans jacoboni2pdf !\nJ'espère que ce petit script vous permettra de ne pas passer 3 heures à récupérer les diapos ;)\n"

#Informations de connexion et de recherche
login="YOURLOGIN"
password="YOURPASSWORD"

if login=="YOURLOGIN" or password=="YOURPASSWORD":

	print "Veuillez changer les variables login et password dans le fichier jacoboni2pdf avant de continuer svp."
	sys.exit(1)
	
pattern_login=re.compile(r'value=\"([0-9A-F]+)\"')
pattern_liens=re.compile(r'(http://umtice.univ-lemans.fr/pluginfile\.php/[0-9]+/mod_lightboxgallery/gallery_images/0/(Diapositive[0-9]{2}\.png))')
lien=raw_input("Veuillez entrer le lien du cours où récupérer les diapositives : ")

#Mise en place du système de gestion des cookies + page web
cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

#Récupération du CSRF token
reponse=opener.open('https://cas.univ-lemans.fr/cas/login?service=http%3A%2F%2Fumtice.univ-lemans.fr%2Flogin%2Findex.php%3FauthCAS%3DCAS')
token=re.search(pattern_login,reponse.read())

#Connexion au site de l'Umtice et récupération de la page du cours
ids={'username':login,'password':password,'_eventId':"submit","submit":"LOGIN","lt":token.group(1)}
donnees=urllib.urlencode(ids)
reponse=opener.open('https://cas.univ-lemans.fr/cas/login?service=http%3A%2F%2Fumtice.univ-lemans.fr%2Flogin%2Findex.php%3FauthCAS%3DCAS',donnees)

print '\nInitialisation de la connexion à l\'UMTICE\n'

#Connexion à la page voulue, récupération des liens et création des fichiers
try:
	reponse=opener.open(lien).read()
	
except urllib2.HTTPError, err:
	
	if err.code==404:
		print "Lien incorrect !"
		sys.exit(1)

#Création du dossier contenant les images
dossier=re.search(r'Cours\s[0-9]', reponse).group(0)
os.makedirs(dossier)

#Téléchargement des images

for lien in re.finditer(pattern_liens, reponse):

	image=opener.open(lien.group(1)).read()
	
	f=open(dossier+'/'+lien.group(2),'w')
	f.write(image)
	f.close
	
	print "Création du fichier ",lien.group(2)

#Conversion
print "\nGénération du pdf\n"

os.chdir(dossier)
cmd="convert -quality 100 Diapositive*.png "+dossier.replace(' ','\\ ')+".pdf"
os.system(cmd)

#Supression des images
print "\nSupression des images téléchargées.\n"

for f in os.listdir("."):
	if re.match(r'Diapositive[0-9]{2}\.png',f):
		os.remove(f)

print "Supression effectuée\n"
print '\nPdf crée à l\'emplacement '+dossier+'/'+dossier+'.pdf'