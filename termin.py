import requests
import time
import datetime
import calendar
from bs4 import BeautifulSoup as bs

# populate the anliegen with the corresponding number appended to each url here: https://service.berlin.de/dienstleistungen/
anliegen = "324269" # "120686", "324269"

# page defaults to 2 months, if you want to paginate to further months you can put the start date here. 
date_filter = datetime.date(2020,10,1)

# locations are hardcoded, note that not every amt is available for every appointment, will error if you look for the wrong amt/leistung combination
locations = {
  "Charlottenburg": "122210,122217,122219,122227",
  "Kreuzberg": "122231,122238,122243",
  "Lichtenberg": "122252,122260,122262,122254",
  "Hellersdorf": "122271,122273,122277",
  "Mitte": "122280,122282,122284",
  "Neukolln": "122291,122285,122286,122296",
  "Pankow": "150230,122301,122297,122294",
  "Reinickendorf": "122312,122314,122304,122311,122309",
  "Spandau": "122281,122279",
  "Steglitz": "122276,122274,122267",
  "Tempelhof": "122246,122251,122257",
  "Treptow": "122208,122226"
}

def print_dates(anliegen, location, dienstleister, run_type):

  response = []
  if run_type == 0:
    url="https://service.berlin.de/terminvereinbarung/termin/restart/?providerList=" + dienstleister.replace(",","%2C") + "&requestList=" + anliegen + "&source=dldb"
  else:
    url="https://service.berlin.de/terminvereinbarung/termin/day/" + str(run_type) + "/?providerList=" + dienstleister.replace(",","%2C") + "&requestList=" + anliegen + "&source=dldb"
  #print(url)
  r = requests.get(url)
  if r.status_code != 200:
    print(location, r.status_code)
    return
  res = r.text
  #
  soup = bs(res, 'html.parser')

  details = soup.find_all("table")
  dates = []
  x = 0
  for detail in details:
    x += 1
    #print(location, detail)
    months = detail.find("th", {"class": "month"})
    if months:
      for i in months.contents:
          month = i
      td = detail.find_all('td')
      link = detail.find("a")
      #print(location, a)
      #buchbar heutemarkierung
      for val in td:
        # if 'class="nichtbuchbar"' not in str(val) and 'class="heutemarkierung"' not in str(val) and 'class=""' not in str(val) and 'class="nichtbuchbar heutemarkierung"' not in str(val) and 'class' in str(val):
        if 'class="buchbar heutemarkierung"' in str(val) or 'class="buchbar"' in str(val):
          for v in val:
            dates.append((location + ": " + str(month) + " - " + str(val.find("a").text)))

  if dates:
    for i in dates:
      response.append(i)
  else:
    response.append("Nothing available for " + location + ".")

  return response

messages = []
d = str(calendar.timegm(date_filter.timetuple()))
for key, value in locations.items():
  m = print_dates(anliegen, key, value, 0)
  if m:
    if m not in messages:
      messages.append(m)
  time.sleep(1)
  m = print_dates(anliegen, key, value, d)
  if m:
    if m not in messages:
      messages.append(m)
  time.sleep(1)

for message in messages:
  for m in message:
    print(m)
