# 1. Introduction

The UCSC extension website is hard to use, especially for choosing courses. The data are scattered around; the naming of the courses is inconsistent; and some key information is either hidden deep in the hierarchy or is nowhere to be found. As an international student, we need to select at least 12 credits per quarter to maintain our status. Combined with a slow internet connection, it is really a pain to find satisfying courses.

# 2. Requirements
 
The program is tested on OS X 10.11 Beta (15A262e) with Python 2.7.8.

It requires `lxml` and `unicodecsv`, both can be installed with `pip`:

    pip install lxml
    pip install unicodecsv

On Ubuntu, you may also need to install additional packages with the following command:

    sudo apt-get install libxml2-dev libxslt1-dev python-dev zlib1g-dev

 
# 3. Description of the Python program

The program is a little bot for crawling the UCSCx course website (http://course.ucsc-extension.edu/modules/shop/index.html) and printing all the courses in csv format.

Here is a sample output:
 

```
id,name,location,start,end,day,time,cost,credit,instructors,catalog,link
3300.(023),Income Tax Accounting,SANTA CLARA,2015-09-16,2015-11-18,3,18:00:00,775.0,4.0,Lynda Renee Boman,Accounting,http://course.ucsc-extension.edu/modules/shop/index.html?action=section&OfferingID=1531861&SectionID=5277259
3658.(149),Introduction to Accounting I: Financial Accounting,ONLINE,2015-09-16,2015-12-09,3,00:00:00,775.0,4.0,Dianne V Conry,Accounting,http://course.ucsc-extension.edu/modules/shop/index.html?action=section&OfferingID=1532219&SectionID=5277244
3658.(150),Introduction to Accounting I: Financial Accounting,SANTA CLARA,2015-09-14,2015-11-16,1,18:00:00,775.0,4.0,Brett M. Layton,Accounting,http://course.ucsc-extension.edu/modules/shop/index.html?action=section&OfferingID=1532219&SectionID=5277248
2057.(021),Certified Bookkeeper Program,SANTA CLARA,2015-09-08,2015-11-21,2,18:00:00,1000.0,7.5,Brett M. Layton,Accounting,http://course.ucsc-extension.edu/modules/shop/index.html?action=section&OfferingID=1530618&SectionID=5275440
...
```

id - the id of the section
name - the name of the offering, e.g. Python for Programmers
location - the location of the section, e.g. ONLINE, SANTA CLARA
start - the start date of the section, e.g. 2015-09-01
end - the end date of the section
day - the day of week of the secction, e.g. 1 (Monday), 7 (Sunday)
time - the time of the section
cost - the cost of the section, e.g. $620, $980
credit - the credit of the section, e.g. 1.5, 3.0
instructors - the instructor list
catalog - 
link - the link to the official section page
 
# 4. Screenshots of the program output  - If you are using a specific hardware and cannot obtain screenshot, please enclose appropriate photographs
 
 
# 5. Conclusion -  Describe in __brief__ the problem you solved, the program you wrote and obtained output.


 
 
# 6. Python program

The source code is available at GitHub: https://github.com/kuanyingchou/ucscx

