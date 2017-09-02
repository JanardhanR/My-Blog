This repository contains the files required to deploy and run the Multi User Blog done as part of the 
Udacity FSND.  


Project files
1. The project solution has 3 .py files and multiple html jinja2 template files and css/image files.
2. pylint has been run and comments addressed except for adding comments where its simple and self explanatory
3. some of the functions used were done as part of excercises in earlier courses and have been reused in the project.

How to open/run the Blog
1. Blog is deployed on GCloud and can be accessed using the below URL
     http://blogpost-173512.appspot.com

2. Blog has been tested for mobile and desktop viewports

3. Signup for a new user or Login using the below userid/passwords to login and try out newpost/comment/edit/like/dislike.
   a.  username -> jana , password -> jana
   b.  username -> banu , password -> banu
   b.  username -> oppo , password -> oppo

How to install the dependencies and run the app locally(Windows)
    Follow the below instructions to download from github and deploy it locally
    
    1. Follow instructions listed in https://cloud.google.com/appengine/docs/standard/python/quickstart
       for installing and configuring Google App Engine
    2. Follow instructions listed in https://cloud.google.com/sdk/docs/#windows for installing up
       the GCould SDK
    3. Download the source from https://github.com/JanardhanR/My-Blog
    4. Navigate to path where main.py is present(...\My-Blog).   
        Start deployment by running below command.  Please note the "." which is required and denotes
        current directory as shown below.
        
            E:\My-Blog> dev_appserver.py .
