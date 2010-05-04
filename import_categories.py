"""
This script imports Google Base's categories into our database from a text file
available at: http://www.google.com/basepages/producttype/taxonomy.txt
"""
#Load Django environment
from django.core.management import setup_environ
import settings
setup_environ(settings)

from myrchme.main_site.models import *


def add_categories(filepath="main_site/googles_categories.txt"):
    """
    add_categories:
    Parses Google's category taxonomy file and adds all the categories to
    Myrchme's databse.
    """
    import csv
    try:
        reader = csv.reader(open(filepath, 'rU'), delimiter='>')
    except IOError:
        print "Could not read file at path: " + filepath
        exit()
    catgs_added = 0

    for line in reader:
        title = line[-1].strip()
        #save the full category path as string e.g. "Animals > Cow > Bull"
        full_title = ""
        for snippet in line:
            full_title += snippet.strip()+ " > "
        full_title = full_title.rstrip(" > ")

        #get the parent category, if there is one
        parent_full_title = ""
        for snippet in line[:-1]:
            parent_full_title += snippet.strip()+ " > "
        parent_full_title = parent_full_title.rstrip(" > ")
        
        if parent_full_title == '': #top-level catagories case
            parent = None
        else:
            parent = Category.objects.get(full_title=parent_full_title)
        
        category, created = Category.objects.get_or_create(
                             title=title,
                             full_title=full_title,
                             parent=parent)
        if(created):
                catgs_added += 1
    print "Categories created: " + str(catgs_added)


#Makes this file into an executable script
#Usage: python import_categories.py <filepath>
if __name__ == "__main__":
    import sys
    try:
        add_categories(sys.argv[1])
    except IndexError: #if no filapath arg given, use default filepath
        add_categories()


    
