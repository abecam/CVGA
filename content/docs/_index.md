---
title: "How to"
description: "How to add yourself to the Collective."

cascade:
  showDate: false
  showAuthor: false
  invertPagination: true
---

{{< lead >}}
How to add yourself to the Collective: studio, service or content creator
{{< /lead >}}

There are initially 2 main ways to add yourself:

- If you don't have experience with GitHub and do not want to deal with it, just contact us (currently cvga@theGiantBall.com) to add yourself.
For studios we have a tool to generate the page, it needs your wanted name and a description for your studio and a list of Steam game ID. 

Friends will often be studio too, so will use the same tool.

For services and content creator, the best is probably a link (could be to a YT channel, a LinkTree, ...), a name and a description. But feel free to give something else.


- If you can and want to use GitHub, you can do a local clone, add your content and to a pull request.

Studios are added in subfolders of content/studios, services in subfolders of content/services, content creatots in subfolders of content/content_creators and friends in subfolders of content/friends.

To add your content:
  - if you are familiar with Hugo, feel free to add a custom content.
  - if you are a studio with game on Steam, a python tool is provided in the folder createPageFromSteam:
    Your data will be in the your_page_infos folder:
      - author_infos.json contain your studio information, but don't change the name of the avatar. You can replace the avatar with your png, but keep the name. If you want a jpg instead, you will have to copy it later in /assets, and change the name in your studio json in /data/authors. The name of the json is the name you provided for your studio (in the info_and_list_of_games.txt file, see next).
      - info_and_list_of_games.txt contains the name of your studio in the first line, then the name of the folder to store the page (in /content/games/, it can be copied to /content/friends/ or /content/services/ afterwards), then the ID of your games, one ID per line.

    Once you have filled the information, simply run createPageFromSteam.py. It needs some libraries which are detailed in requirements.txt
  - otherwise, it is best to see the existing pages in /content/content_creators or /content/services/ afterwards or /content/friends/ to create your.
  For instance, to create a new page as a content_creators, if there is one existing folder "one_streamer", copy the full folder. Now inside the folder you should change the feature image (which need to start by "feature" and can be a jpg or a png) or at least remove it, then edit the index.md file.
  The index.md file start with general information, then with some content. 
  If an externalUrl is given, the page will not be shown and clicking on the thumbnail in the top page will go to the given url.

You can see the resulting webpage by installing and running <a target="_blank" href="https://gohugo.io/">Hugo</a>. Otherwise I will check it myself.
Once you are happy with your changes, simply do a pull-request (you will need your own fork).