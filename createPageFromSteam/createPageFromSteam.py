import json
from datetime import datetime
import traceback

import requests
import os
import shutil

from slugify import slugify

def update_one_from_steam(id, name_of_folder, studio_name=""):
    # Using a file containing App id and desired folder name
    # comma separated -> All in one page
    # on a new line -> create a new page (new folder)

    print(f"Will try to fetch using id {id} for {name_of_folder}");
    if id:
        # check if Steam ID
        # Fetch JSON data from the API endpoint
        api_endpoint = f"https://store.steampowered.com/api/appdetails?appids={id}"
        response = requests.get(api_endpoint)
        if response.status_code == 200:
            # Load the JSON data
            data = response.json()
            # Check if success is true
            subdata = data[f"{id}"]
            success = subdata['success']
            if not success:
                print("Failed to fetch data from Steam, check the ID.")
                return

            content = subdata['data']

            # Check if updating or creating
            try:
                if not os.path.isfile("index.md"):
                    print(f"The main page does not exist yet, something went wrong before, please try again")
                    return

                writeDataFromSteam(name_of_folder, content, id)
            except Exception as exception:
                print("Sorry, something went wrong", exception)
                print(traceback.format_exc())

def addStudioInfo(studio_name, name_of_folder):
    with open("index.md", "a", encoding="utf-8") as main_page:
        main_page.write("---\n")
        main_page.write(f"title: \"{studio_name}\"\n")
        main_page.write("date: "+datetime.today().strftime("%Y-%m-%d"))
        main_page.write("\nshowAuthor: false")
        main_page.write("\nauthors:\n - \""+name_of_folder+"\"")
        main_page.write("\n---")
        main_page.write("\n")
        main_page.write(f"# {studio_name}\n")

def writeDataFromSteam(name_of_folder, content, id):
    # Create Video Game from JSON data

    # First check if not >18 - required_age	"18"
    if content['required_age'] == "18":
        print(f"Sorry, no mature content in the filter shop. {content['name']} cannot be added.")
        return
    # Missing: game type, studio, publisher, platforms, vignette, link to shop (should be obvious)

    # creating images
    # header_image

    # capsule_image
    #
    addCapsuleAndHeader(content['name'],content['capsule_image'], content['header_image'])

    # screenshots
    # screenshots
    #   0
    #   id	0
    # path_thumbnail	"https://cdn.akamai.steamstatic.com/steam/apps/1378660/ss_509aa0dc74d06b8a3544d62f2fd5b0b235c2ab84.600x338.jpg?t=1687509345"
    # path_full	"https://cdn.akamai.steamstatic.com/steam/apps/1378660/ss_509aa0dc74d06b8a3544d62f2fd5b0b235c2ab84.1920x1080.jpg?t=1687509345"
    addAllThumbnails(content['name'],content['screenshots'])

    addGeneralInfo(name=content['name'], description=content['short_description'],
                                         url=content['website'])

    # studio(s) and publisher(s)
    addStudioAndPublisher(content['developers'], content['publishers'])

    #
    addPlatforms(content['platforms'])

    # Categories
    if 'genres' in content:
        addCategories(content['genres'])

    # And the link to Steam
    addLinkToSteam(id)

    # link to shop: f"https://store.steampowered.com/app/{id}"
    print("Information fetched successfully.")


def addCapsuleAndHeader(game_name, capsule_url, header_url):
    usable_name = slugify(game_name)
    # Stream the image from the url
    response = requests.get(capsule_url, stream=True)

    os.chdir("img")

    # Was the request OK?
    if response.status_code == requests.codes.ok:


        # Get the filename from the url, used for saving later
        file_name = f"{usable_name}_capsule.jpg"

        # Create a temporary file
        with open(file_name, 'wb') as output:

            # Read the streamed image in sections
            for block in response.iter_content(1024 * 8):

                # If no more file then stop
                if not block:
                    break

                # Write image block to temporary file
                output.write(block)


    # Stream the image from the url
    response = requests.get(header_url, stream=True)

    # Was the request OK?
    if response.status_code == requests.codes.ok:
        # Get the filename from the url, used for saving later
        # Check if the feature image already exist, otherwise we add it as well
        file_name = f"{usable_name}_head.jpg"

        # Create a temporary file
        with open(file_name, 'wb') as output:

            #r = requests.get(url)
            # Read the streamed image in sections
            for block in response.iter_content(1024 * 8):

                # If no more file then stop
                if not block:
                    break

                # Write image block to temporary file
                output.write(block)

        os.chdir("..")
        # Check if the feature image already exist, otherwise we add it as well
        file_name_feature = "feature.jpg"

        if not os.path.isfile(file_name_feature):
            #BASE_PATH = os.path.dirname(os.path.realpath(__file__))

            shutil.copyfile("img/"+file_name, file_name_feature)

    with open("index.md", "a", encoding="utf-8") as main_file:
        main_file.write(f"\n![Header](img/{file_name})\n")
        #main_file.write(f"\n![Capsule](img/capsule.jpg)\n")
def addAllThumbnails(game_name, thumbnails):
    usable_name = slugify(game_name)

    with open("index.md", "a", encoding="utf-8") as main_file:
        main_file.write("\n{{< gallery >}}\n")

    os.chdir("img")


    for nb_thumbnail, one_entry in enumerate(thumbnails):
        image_url = one_entry['path_thumbnail']

        # Stream the image from the url
        response = requests.get(image_url, stream=True)

        # Was the request OK?
        if response.status_code != requests.codes.ok:
            # Nope, error handling, skip file etc etc etc
            continue

        # Get the filename from the url, used for saving later
        file_name = f"{usable_name}_thumbnail_{nb_thumbnail}.jpg"

        with open(file_name, 'wb') as output:

            # Read the streamed image in sections
            for block in response.iter_content(1024 * 8):

                # If no more file then stop
                if not block:
                    break

                # Write image block to temporary file
                output.write(block)
        # And add to the gallery
        with open("../index.md", "a", encoding="utf-8") as main_file:
            main_file.write(f"<img src=\"img/{file_name}\" class=\"grid-w50\" />\n")

    os.chdir("..")
    with open("index.md", "a", encoding="utf-8") as main_file:
        main_file.write("{{< /gallery >}}\n")

def addGeneralInfo(name, description, url):
    with open("index.md", "a", encoding="utf-8") as main_page:
        main_page.write("\n\n")
        main_page.write("## "+name)
        main_page.write("\n\n")
        main_page.write(description)

def addStudioAndPublisher(developers, publishers):
    with open("index.md", "a", encoding="utf-8") as main_page:

        #for one_entry in developers:
         #   main_page.write("\n")
         #   main_page.write(f"## Developed by {one_entry}\n")

        for one_entry in publishers:
           main_page.write("\n\n")
           main_page.write(f"### Published by {one_entry}\n")


def addPlatforms(platforms):
    with open("index.md", "a", encoding="utf-8") as main_page:
        main_page.write("\n\n")
        # currently only a boolean for Windows, Linux and Mac
        if platforms['windows']:
            main_page.write("Windows")
        if platforms['linux']:
            main_page.write("Linux")
        if platforms['mac']:
            main_page.write("Mac")

def addCategories(genres):
    with open("index.md", "a", encoding="utf-8") as main_page:
        main_page.write("\n\nGenres: ")
        is_first = True
        for one_entry in genres:
            if not is_first :
                main_page.write(", ")
            else :
                is_first = False
            main_page.write(one_entry['description'])

def addLinkToSteam(steam_id):
    url = f"https://store.steampowered.com/app/{steam_id}"

    with open("index.md", "a", encoding="utf-8") as main_page:
        main_page.write(f"\n\n<a target=\"_blank\" href=\"{url}\">See on Steam</a>")

# Press the green button in the gutter to run the script.
def generateFromListOfGamesAndStudioName():
    with open("your_page_infos/info_and_list_of_games.txt", "r") as source_file :
        studio_name = source_file.readline().rstrip()
        name_of_folder = source_file.readline().rstrip()

        os.chdir("../content/games/")
        if os.path.isdir(name_of_folder):
            print(f"Sorry, the folder {name_of_folder} already exists")
            return
        os.makedirs(name_of_folder)
        os.chdir(name_of_folder)
        addStudioInfo(studio_name, name_of_folder)
        os.makedirs("img")

        # Copy the author info and the avatar, change the avatar name.
        author_json_file_name = f"../data/authors/{name_of_folder}.json"
        avatar_file_name = f"{name_of_folder}_avatar.png";
        os.chdir("../../../createPageFromSteam/")
        with open("your_page_infos/author_info.json") as author_info :
            data_author = json.load(author_info)
            data_author["image"] = "img/" + avatar_file_name

            with open(author_json_file_name, 'w') as json_file:
                json.dump(data_author, json_file)


        shutil.copyfile("your_page_infos/your_avatar.png", "../assets/img/" + avatar_file_name)

        os.chdir("../content/games")
        os.chdir(name_of_folder)

        while id := source_file.readline().rstrip():
            update_one_from_steam(id, name_of_folder, studio_name="")

if __name__ == '__main__':
    generateFromListOfGamesAndStudioName()