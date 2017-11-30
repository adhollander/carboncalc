# carboncalc
Tools to calculate growth statistics for individual urban trees such as for estimating carbon storage.

This repository contains code to calculate greenhouse gas and emissions 
benefits of individual urban trees given data on parameters such as tree species, 
geographic region, tree diameter, and tree height. This work comes from a project funded by CalFire and the US Forest Service
to assess the benefits of California's urban trees, and builds upon a set of allometric equations for urban tree growth published 
as a USFS General Technical Report ([McPherson, Van Doorn, and Peper 2016](https://www.treesearch.fs.fed.us/pubs/52933)).
A publication describing the California urban tree project is: McPherson, E. Gregory, Qingfu Xiao, Natalie S. van Doorn, John de Goede, Jacquelyn Bjorkman, Allan Hollander, Ryan M. Boynton, James F. Quinn, and James H. Thorne. 2017. “The Structure, Function and Value of Urban Forests in California Communities.” _Urban Forestry & Urban Greening_ 28 (Supplement C):43–53. https://doi.org/10.1016/j.ufug.2017.09.013.


There are three major pieces in this repository. The first is the core Python code (```biomass.py``` and ```growth.py``` connecting to the
SQLite database ```UrbanForestCC.sqlite```) containing the functions for calculating tree biomass and growth. The second piece, 
contained in the directory carboncalc, is a RESTful API for querying the core calculator code, written
using the [Django REST framework](http://www.django-rest-framework.org/). This API is described in the document [ccAPI.pdf](https://github.com/adhollander/carboncalc/blob/master/ccAPI.pdf). Detailed instructions for installing and using 
the code are given below. The third piece is contained in the directory ccshiny and is a prototype of a user interface to this API 
developed using the R/Shiny platform. **All contents of this repository are released into the public domain.**

## Python carbon calculator code.

   The key files here are ```biomass.py```, ```growth.py```, and ```UrbanForestCC.sqlite```. To execute these Python modules, the libraries numpy
   scipy need to be installed. Also, the pathnames in both biomass.py and growth.py to the UrbanForestCC.sqlite database needs to 
   be changed to the correct location on one's system. Important functions in these modules are the following:

  * **biomass.py**: ```biomass_calc```

  * **growth.py**: ```age_calc2, biomass_diff2, inv_age_calc2```
  
## Django RESTful API
   
   The files in the directory carboncalc contain the Python code for building a RESTful API to the functions in ```biomass.py``` and
   ```growth.py```. Additionally the API supports calculating avoided emissions reductions from trees shading buildings. The API is
   described in the file [ccAPI.pdf](https://github.com/adhollander/carboncalc/blob/master/ccAPI.pdf). This application has been developed using the [Django REST framework](http://www.django-rest-framework.org/), and Django experience 
   is needed to install and run this API. 
 
## Installation Outline

The following gives a overview of how to install the Django RESTful API.

1. Create python virtual environment.

    ```$ virtualenv carboncalc```

2. Install django in environment

    ```$ cd carboncalc
    $ source bin/activate
    $ pip install django
    ```

3. Get the carboncalc code from github

e.g.
    ```$ wget https://github.com/adhollander/carboncalc/archive/master.zip
    $ unzip master.zip
    $ cd carboncalc-master/carboncalc
    ```

4. Install needed libraries.

    ```$ pip install django-bootstrap3
    $ pip install djangorestframework # is version 3 the right version?
    $ pip install numpy
    $ pip install scipy # need gfortran
    ```

5. Copy ```carboncalc/settings_secret_template.py``` to ```carboncalc/settings_secret.py```.

6. Create a key for  ```settings_secret.py```. One way to generate this is to use the Django key generator application at http://www.miniwebtool.com/django-secret-key-generator/. For test purposes, change DEBUG to True in  ```settings_secret.py```.

7. Create symlinks to ```biomass.py``` and ```growth.py``` in ```carboncalc-master``` to ```carboncalc-master/carboncalc/biomass.py``` and ```carboncalc-master/carboncalc/growth.py```.

8. Adjust pathnames in ```biomass.py``` and ```growth.py``` to  ```UrbanForestCC.sqlite``` file.



9. Test the application with python manage.py runserver. (You may get this warning which can be ignored: ```You have 13 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions. 
Run 'python manage.py migrate' to apply them settings_secret.py```)

10. Sample query: http://127.0.0.1:8000/api/bmasstoCO2?biomass=7.  See https://github.com/adhollander/carboncalc/blob/master/ccAPI.pdf for more queries.
