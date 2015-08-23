import requests
from lxml import etree, html
import re
import datetime
import time
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               'Host': 'course.ucsc-extension.edu',
               'Referer': 'http://course.ucsc-extension.edu/modules/shop/index.html'}

def get_section_dict():
# searchOfferings.action
    url = 'http://course.ucsc-extension.edu/modules/shop/searchOfferings.action'
    params = {
        'CatalogID': 80,
        'startPosition': 0,
        'pageSize': 100
    }
    r = requests.get(url, params=params, headers=headers)
    xml = etree.fromstring(r.content)
    sections = xml.xpath('//Section')

    os = {}
    for s in sections:
        oid, sid = s[1].text, s[2].text
        if oid in os:
            os[oid].append(sid)
        else:
            os[oid] = [sid]

    # print os
    return os

def to_field(elem):
    if not elem:
        return None
    elif isinstance(elem, list):
        return ';'.join(e.text for e in elem 
                if e is not None and e.text is not None)
    else:
        return elem.text

def get_date(t):
    m = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', t)
    if m:
        y, m, d = m.group(1), m.group(2), m.group(3)
        return datetime.datetime(year=int(y), month=int(m), day=int(d)) #'%s-%s-%s' % (y, m, d)
    else:
        return None

def get_time(t):
    m = re.search(r'\d{2}:\d{2}:\d{2}', t)
    if m:
        return m.group(0)
    else:
        return None

def get_sections():
    # offeringOverview.action
    # defaultSections.action
    url = 'http://course.ucsc-extension.edu/modules/shop/defaultSections.action'

    os = get_section_dict()
    for k, v in os.iteritems():
        oid = k
        
        r = requests.get(
    'http://course.ucsc-extension.edu/modules/shop/offeringOverview.action',
    {'OfferingID': oid},
    headers=headers)
        xml = etree.fromstring(r.content)
        name = xml.xpath('//Offering/Name')

        for sid in v:

            params= {
                'OfferingID': oid,
                'SectionID':sid
            }

            r = requests.get(url, params=params, headers=headers)
            xml = etree.fromstring(r.content)


            active = xml.xpath('//IsActive')
            if not active:
                continue

            section = {}
            section['name'] = to_field(name)
            section['id'] = to_field(xml.xpath('//data/Section/SectionNumber'))
            section['location'] = to_field(xml.xpath('//SiteName'))

            start_date = xml.xpath('//StartDate')
            start_date_field = to_field(start_date)
            d = get_date(start_date_field)
            section['start'] = d.strftime('%Y-%m-%d')
            section['day'] = d.isoweekday()
            section['time'] = get_time(start_date_field)

            end_date = xml.xpath('//EndDate')
            d = get_date(to_field(end_date))
            section['end'] = d.strftime('%Y-%m-%d')

            section['instructors'] = to_field(xml.xpath('//InstructorName'))
            section['cost'] = to_field(xml.xpath('//Cost'))
            section['credit'] = to_field(xml.xpath('//CreditHours'))

            # description = xml.xpath('//Description');
            # print html.fromstring(to_field(description)).text_content()

            print section
        # time.sleep(0.5)
        break
