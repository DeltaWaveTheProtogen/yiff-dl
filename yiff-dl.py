from posixpath import join as urljoin
from bs4 import BeautifulSoup as bs
from urllib.parse import unquote
from io import BytesIO
from PIL import Image
from sys import argv
import requests
import img2pdf
import json
import time
import os


USER_AGENT_YIFFER = "Yiffer-dl V0 <notandinotandi@gmail.com> (bot)"
USER_AGENT_E621 = "Monosodium/10.0 (DeltaWave0x)"


    
if len(argv) < 2:
    print("I want at least one full URL!!")
    exit(1)



def main():
    URL = argv[1:]
    if "-b" in URL[0]:
         with open(argv[2]) as f:
             URL_LIST = [line.rstrip() for line in f]
             for link in URL_LIST:
                 if "e621.net" in link:
                     download_comic_e621(link)
                 elif "yiffer.xyz" in link:
                    download_comic_yiffer(link,USER_AGENT_YIFFER)
    else:
        for link in URL:
            if "e621.net" in link:
                download_comic_e621(link)
            elif "yiffer.xyz" in link:
                 download_comic_yiffer(link,USER_AGENT_YIFFER)
    



#YIFFER
def download_comic_yiffer( url,user_agent=USER_AGENT_YIFFER):
    image_id = 1
    err = None

    dl_path = url.split("/")[-1]
    dl_path = unquote(dl_path)

    print("Downloading " + dl_path + " from Yiffer.xyz: ")
    os.mkdir(dl_path)
    while err is None:
        # form: ../comics/<name>/xx.jpg
        image_src = urljoin("../comics/", url.split("/")[-1], "{0:02d}.jpg".format(image_id))
        print("\t" + "Image {} downloaded".format(image_id))

        err = _download_image_yiffer(url, dl_path, image_id, image_src)
        image_id = image_id + 1


def _download_image_yiffer(comic_url, dl_dir, image_id, image_src):
    image_url = urljoin(comic_url, image_src)

    # Download path should be ./dl/xx.jpg
    dl_path = os.path.join(dl_dir,"{0:02d}.jpg".format(image_id))

    # Actually get the image data
    image_data = requests.get(image_url)

    if image_data.status_code != 200:
        print("Image {}: Status code: {}" .format(image_id, image_data.status_code))
        return image_data.status_code

    with open(dl_path, "wb") as f:
        f.write(image_data.content)
        





#E621
def download_comic_e621(url):
    
    ID = url.split("/")[-1]


    headers = {
        "User-Agent": USER_AGENT_E621
        }

    #Json form for intial Pool Search
    form = {
          'search[id]': ID
        }

    #Intial Pool GET Request
    page = requests.get("https://e621.net//pools.json",headers=headers, data = form)

    if page.status_code == "200" :
        print("> Sorry, the pool doesn't seem to exist")
        exit()
        
    json_response = json.loads(page.text)

    #Here The code takes the posts' IDs out of the json response
    ids = json_response[0]['post_ids'];

    #Get Pool's name and create a directory for it
    path = json_response[0]["name"]
    dicto = {'>': ' ',
             '<': ' ',
             ':': ' ',
             '|': ' ',
             '?': ' ',
             '*': ' ',
             '"': ' '
             }
    path = path.translate(str.maketrans(dicto))
    os.mkdir(path)

    extensions = (".jpg",".jpeg",".png")

    print("Downloading " + path + " from E621.net: ")
    #Iterate over the ID list
    for x in range(len(ids)):

        #GET request Post by using the ID found before
        post_link = requests.get("https://e621.net/posts/" + str(ids[x]), headers=headers)

        #Parse html
        soup = bs(post_link.text, 'html.parser')

        #Here I'm searching for all the href lines that start with https://static1.e621.net and end with and image extension. The code is ugly, but works
        for link in soup.findAll('a'):
            
            if (((str(link.get('href')).startswith("https://static1.e621.net/")) and ((str(link.get('href')).endswith(extensions))))):
                
                image = Image.open(BytesIO(requests.get(link.get('href')).content))
                image.save(path + "/page"+ str(x)+ ".png" , "PNG")
                print("\t" + "Image " + str(x) + " downloaded")
                break



if __name__ == "__main__":
    main()


