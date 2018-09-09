import csv
import time
import os
import sys
import random

# THIRD PARTY LIBRARIES
import requests
from bs4 import BeautifulSoup

def make_directory():
	directory_name = "ipl_data"
	while directory_name in os.listdir():
		directory_name = "ipl_data_{}".format(random.randint(1,200))
	os.mkdir(directory_name)
	print("Directory with name {} created.".format(directory_name))
	return directory_name

print("Request recieved, please check folder named 'ipl_all-time_data' at current directory after atleast 2 minutes.")

homepage_url = "https://www.iplt20.com/stats/all-time"

homepage = requests.get(homepage_url)
if homepage.status_code != 200:
	print(r.reason)
	sys.exit()

homepage_soup = BeautifulSoup(homepage.text, 'html.parser')

target_urls = []
try:
	for atag in homepage_soup.find_all('a'):
		chunks = atag.get('href')
		if not chunks:
			continue
		chunks = chunks.split('/')
		if "all-time" in chunks and chunks[-1] != "" and chunks[-1] != "all-time":
			target_urls.append(atag.get('href'))
except Exception as e:
	print("Error ->", e)
	sys.exit()

directory_name = make_directory()

try:
	for site_url in target_urls:
		time.sleep(2)
		r = requests.get("https://www.iplt20.com"+site_url)

		soup = BeautifulSoup(r.text, 'html.parser')
		data_table = soup.find('table')
		rows = data_table.find_all('tr')

		column_names = []

		for theaders in rows[0].find_all('th'):
			column_names.append(theaders.attrs.get('title'))
		column_names[1] = "Players"

		file_name = "{}/{}.csv".format(directory_name, site_url.split("/")[-1])
		with open(file_name,'w') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(column_names)
			for row in rows:
				column_data = []
				for tdata in row.find_all('td'):
					column_data.append(" ".join(tdata.text.strip().split()))
				writer.writerow(column_data)
		print("#", end='', flush=True)
except Exception as e:
	print("Error =====> ", e)

print("Completed.")