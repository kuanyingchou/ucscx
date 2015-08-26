from __future__ import print_function # 7. Importing external modules
import requests 
from lxml import etree, html
import re
import datetime
import time
import unicodecsv
import sys

URL_BASE = 'http://course.ucsc-extension.edu/modules/shop'
URL_OFFERING = '/offeringOverview.action'
URL_SECTION = '/defaultSections.action'
URL_CATALOG = '/searchOfferings.action'
URL_ALL = '/courseCatalogs.action'
URL_CATALOG_NAME='/catalog.action'

def get(path, params):
    # 8. Error checks using try-except
    try: 
        return requests.get(URL_BASE + path, params = params)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit()

def get_catalog_ids(): # 4. Functions
    """ return all catalog ids in a list """
    r = get(URL_ALL, params={})
    xml = etree.fromstring(r.content)
    catalogs = xml.xpath('//Catalog/CatalogID')
    return [int(c.text) for c in catalogs]  # 2. list comprehension

def get_offering_section_dict(cid):
    """ construct a dictionary of offering ->* section """
    params = {
        'CatalogID': cid,
        'startPosition': 0,
        'pageSize': 500 # should be enough
    }
    r = get(URL_CATALOG, params=params)
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

def to_str(elem):
    """ create a string from the return value of xpath() """
    if not elem:
        return None
    elif isinstance(elem, list):
        return ';'.join(e.text for e in elem 
                if e is not None and e.text is not None)
    else:
        return elem.text

def get_date(t):
    """ create a date from the date time string """

    m = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', t) # 10. Regular expression
    if m:
        y, m, d = m.group(1), m.group(2), m.group(3)
        return datetime.datetime(year=int(y), month=int(m), day=int(d)) 
    else:
        return None

def get_time_str(t):
    """ get the time part from the date time string """
    m = re.search(r'\d{2}:\d{2}:\d{2}', t)
    if m:
        return m.group(0)
    else:
        return None

def get_section(oid, sid):
    """ return a dictionary from section data """

    params= {
        'OfferingID': oid,
        'SectionID':sid
    }

    r = get(URL_SECTION, params=params)
    xml = etree.fromstring(r.content)


    active = xml.xpath('//IsActive')
    if not active:
        return None

    section = {}
    section['id'] = to_str(xml.xpath('//data/Section/SectionNumber'))
    section['location'] = to_str(xml.xpath('//SiteName'))

    start_date = xml.xpath('//StartDate')
    start_date_field = to_str(start_date)
    d = get_date(start_date_field)
    if d is not None:
        section['start'] = d.strftime('%Y-%m-%d')
        section['day'] = d.isoweekday()
    t = get_time_str(start_date_field)
    if t is not None:
        section['time'] = t

    end_date = xml.xpath('//EndDate')
    d = get_date(to_str(end_date))
    if d is not None:
        section['end'] = d.strftime('%Y-%m-%d')

    section['instructors'] = to_str(xml.xpath('//InstructorName'))
    section['cost'] = to_str(xml.xpath('//Cost'))
    section['credit'] = to_str(xml.xpath('//CreditHours'))
    section['link'] = 'http://course.ucsc-extension.edu/modules/shop/index.html?action=section&OfferingID=%s&SectionID=%s' % (oid, sid)

    # description = xml.xpath('//Description');
    # print html.fromstring(to_str(description)).text_content()

    # print section
    return section

def get_catalog_name(cid):
    r = get(URL_CATALOG_NAME, {'CatalogID': cid })
    xml = etree.fromstring(r.content)
    return to_str(xml.xpath('//data/Catalog/Name'))

def get_offering_name(oid):
    r = get(URL_OFFERING, {'OfferingID': oid})
    xml = etree.fromstring(r.content)
    return to_str(xml.xpath('//Offering/Name'))

def get_sections(cid):

    os = get_offering_section_dict(cid)

    for oid, sid_list in os.iteritems():
        
        name = get_offering_name(oid)
        # print name

        for sid in sid_list:
            s = get_section(oid, sid)
            if not s:
                continue
            s['name'] = name
            yield s;

        time.sleep(0.2) # be a good boy; don't stress the server

def get_all_sections():
    print('building index...', file=sys.stderr)
    cids = get_catalog_ids()
    oc = {} # offering to catalog names
    os = {} # offering to sections
    count = 0
    for cid in cids:
        cname = get_catalog_name(cid)
        cos = get_offering_section_dict(cid) # offering to sections in a catalog
        for oid in cos:
            if oid in oc:
                oc[oid].append(cname)
            else:
                oc[oid] = [cname]

            if oid not in os:
                os[oid] = cos[oid]
            # print(oid)
        count += 1
        print('\r%d/%d completed' % (count, len(cids)), file=sys.stderr, end='')

    print(file=sys.stderr)
    # print(os)
    # print(oc)
    
    for oid, sids in os.iteritems():
        oname = get_offering_name(oid)
        for sid in sids:
            s = get_section(oid, sid)
            if not s:
                continue
            s['name'] = oname
            s['catalogs'] = ';'.join(oc[oid])
            yield s;
        time.sleep(0.2) # be a good boy; don't stress the server


if __name__ == '__main__':

    writer = unicodecsv.DictWriter(sys.stdout, [
        'id', 'name', 'location', 'start', 'end', 'day', 
        'time', 'cost', 'credit', 'instructors', 'catalogs', 'link' ])
    writer.writeheader()

    for s in get_all_sections():
        writer.writerow(s)


