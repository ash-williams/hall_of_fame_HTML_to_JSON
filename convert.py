from bs4 import BeautifulSoup
import json

ifile = open("halloffame.txt")
html = ifile.read()
ifile.close()

soup = BeautifulSoup(html, "html.parser")

rows = soup.find_all("tr")

print(len(rows))

res_dict = {}

for row in rows:
    #print(row)
    cells = row.find_all("td")
    if len(cells) > 0:
        
        # Year
        year = cells[0].string.strip()

        # Image
        image_data = cells[1]
        try:
            title = image_data.img["alt"]
            source = "http:" + image_data.img["src"]
            image = {
                "title": title, 
                "source": source
            }
        except:
            image = {}
        
        # Band
        name = cells[2].find_all("a")[0].string
        url = "http://wikipedia.org" + cells[2].find_all("a")[0]["href"]
        band = {
            "name": name,
            "url": url
        }

        # Inducted members
        members = cells[3].find_all("a")

        inducted_members = []

        for member in members:
            name = member.string
            url = "http://wikipedia.org" + member["href"]
            if not name.startswith("["):
                inducted_members.append({
                    "name": name,
                    "url": url
                })
        
       
        # Inducted by
        inductor = cells[4].find_all("a")
        if len(inductor) > 0:
            inductor = inductor[0] 
            name = inductor.string
            url = "http://wikipedia.org" + inductor["href"]

            inducted_by = {
                "name": name,
                "url": url
            }

        else:
            inducted_by = {}
        


        inductee = {
            "image": image,
            "band": band,
            "inducted_members": inducted_members,
            "inducted_by": inducted_by
        }

        if year in res_dict.keys(): 
            res_dict[year].append(inductee)
        else:
            res_dict[year] = [inductee]

# Now write it out
ofile = open("hall_of_fame.json", "w")

ofile.write(json.dumps(res_dict))

# ofile.write("[\n")

# for key in res_dict.keys():
#     ofile.write("{")
#     ofile.write("\"{0}\" : {1}".format(key, res_dict[key]))
#     ofile.write("},\n")



# ofile.write("]")
ofile.close()
