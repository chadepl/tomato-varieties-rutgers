"""Downloads dataset from https://njaes.rutgers.edu/tomato-varieties/
"""

# document.getElementsByClassName("menu-list")

# menu-list > li > a => href

# 
# https://njaes.rutgers.edu/tomato-varieties/variety.php?A+Grappoli+D%27Inverno


# id=main-content > p

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://njaes.rutgers.edu/tomato-varieties/"


if __name__ == "__main__":
    print("Starting ... ")

    tomato_dataset = []

    response = requests.get("https://njaes.rutgers.edu/tomato-varieties/")

    if response.status_code == 200:

        print("Success")
        soup = BeautifulSoup(response.text, "html.parser")

        menu_list = soup.find_all("ol", {"class", "menu-list"})

        links = []
        for ol in menu_list:            
            links += ol.find_all("li")

        for i, l in enumerate(links):
            links[i] = l.find("a", href=True)


        for i, l in enumerate(links):
            print(f"{i}")
            dataset_entry = dict(name=l.text, link=BASE_URL + l["href"], comments="")

            response_variety = requests.get(dataset_entry["link"])

            if response_variety.status_code == 200:
                print(f"- Processing info for {dataset_entry["name"]}")
                soup_variety = BeautifulSoup(response_variety.text)
                # id=main-content > p
                div = soup_variety.find_all("div", {"id": "main-content"})[0]
                tomato_properties = div.findChildren("p", recursive=False)
                for prop in tomato_properties:
                    print(prop.text)
                    if ":" in prop.text:
                        prop_name = prop.text.split(":")[0].strip()
                        prop_value = prop.text.split(":")[1].strip()
                        dataset_entry[prop_name] = prop_value
                    else:
                        dataset_entry["comments"] += "No information; "
                        break
            else:
                print(f"- No info for {dataset_entry["name"]}")
                #soup.findChildren

                
            tomato_dataset.append(dataset_entry)
            # break


        tomato_df = pd.DataFrame(tomato_dataset)
        print(tomato_df.head())

        tomato_df.to_csv("tomato_rutgers.csv")