# 1. Introduction

The UCSCx website is hard to use, especially for choosing courses. The data are scattered around; the naming of the courses is inconsistent; and some key information is either hidden deep in the hierarchy or is nowhere to be found. As an international student, we need to select at least 12 credits per quarter to maintain our status. Combined with a slow internet connection, arranging a satisfying schedule is really a pain.

However, I don't want to create another UCSCx website. I'm only interested in the data, since data can be freely filtered, sorted, manipulated, transformed, and analyzed. An interface, on the other hand, is like a viewfinder, only provides incomplete pictures. By decoupling data from user interfaces, we may put them into better use. We may even put different interfaces upon it to tackle different issues.

Thus, I would like to use Python to scrape all the courses from the UCSCx website!

# 2. Requirements
 
The program is tested on OS X 10.11 Beta (15A262e) with Python 2.7.8.

It requires `lxml` and `unicodecsv`, both can be installed with `pip`:

    pip install lxml
    pip install unicodecsv

On Ubuntu, you may also need to install additional packages with the following command:

    sudo apt-get install libxml2-dev libxslt1-dev python-dev zlib1g-dev

 
# 3. Description of the Python program

The program is a little bot that crawls the UCSCx course website (http://course.ucsc-extension.edu/modules/shop/index.html) and prints all the courses in csv format.

UCSCx course website has many catalogs (or programs), and a catalog has many offerings. An offering may be shared among multiple catalogs. Finally, an offering has many sections. Each section has different schedules, locations, etc., and may be taught by different sets of instructors. For example, "Python for Programmers" is an offering. It is considered part of 4 catalogs: Computer Programming, Information Technology, Internet Programming and Development, and Linux. At the time of writing, it has 9 sections, each taught with different schedules.

There are mainly two ways to find a specific course on the website: browse and search. To browse courses, we start with "Course Catalogs", click a catalog, click an offering ID, then click a section. 3 levels of hierarchy.

To search a course, we can specify words or phrases contained in offering names or descriptions, or provide a date range. 

We can start crawling from the search page, but the catalog information would be lost, since neigher the search page nor the search results contain information about catalogs. So the bot goes with the browsing page.

For the implementation, I use Chrome to find out interesting XHR requests, their headers and response; use package `requests` to fetch the results; then use lxml and XPath to parse xml responses.

For the program output, I would like to embrace Unix philosophy and print the result directly to stdout, which can be piped to other tools or redirected to a file. Here is a sample output:

```
id,name,location,start,end,day,time,cost,credit,instructors,catalog,link
3300.(023),Income Tax Accounting,SANTA CLARA,2015-09-16,2015-11-18,3,18:00:00,775.0,4.0,Lynda Renee Boman,Accounting,http://course.ucsc-extension.edu/modules/shop/index.html?action=section&OfferingID=1531861&SectionID=5277259
3658.(149),Introduction to Accounting I: Financial Accounting,ONLINE,2015-09-16,2015-12-09,3,00:00:00,775.0,4.0,Dianne V Conry,Accounting,http://course.ucsc-extension.edu/modules/shop/index.html?action=section&OfferingID=1532219&SectionID=5277244
3658.(150),Introduction to Accounting I: Financial Accounting,SANTA CLARA,2015-09-14,2015-11-16,1,18:00:00,775.0,4.0,Brett M. Layton,Accounting,http://course.ucsc-extension.edu/modules/shop/index.html?action=section&OfferingID=1532219&SectionID=5277248
2057.(021),Certified Bookkeeper Program,SANTA CLARA,2015-09-08,2015-11-21,2,18:00:00,1000.0,7.5,Brett M. Layton,Accounting,http://course.ucsc-extension.edu/modules/shop/index.html?action=section&OfferingID=1530618&SectionID=5275440
...
```
The first line contains the column names:

- id: the id of the section
- name: the name of the offering, e.g. Python for Programmers
- location: the location of the section, e.g. ONLINE, SANTA CLARA
- start: the start date of the section, e.g. 2015-09-01
- end: the end date of the section
- day: the day of week of the secction, e.g. 1 (Monday), 7 (Sunday)
- time: the time of the section
- cost: the cost of the section, e.g. $620, $980
- credit: the credit of the section, e.g. 1.5, 3.0
- instructors: the instructor list
- catalog: catalogs that contain this section
- link: the link to the official section page
 
# 4. Screenshots of the program output  

It's a console program that produces data:

Courses data imported to Google Sheet:
 
 
# 5. Conclusion

After the project completed, we are able to answer some interesting questions:

- How many courses are there?
- What is the cheapest course out there?
- Which courses require least amount of time to take?
- Does this instructor teach other courses?
- I want a Friday course with 3 credits, and the instructor's name starts with an 'R'. What options do I have?

 
# 6. Python program

The source code is available at GitHub: https://github.com/kuanyingchou/ucscx

