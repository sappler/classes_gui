import requests
import math
import pandas as pd
from selectolax.parser import HTMLParser


#a scraper to get a range of apps from the steam store, capturing price, year, reviews, vr support, tags
def main():
    csv = open("db.csv",'a')
    csv.write('course_division,course_number,course_title,description,instructors,quarters\n')
    src = gettext("https://catalog.ucsc.edu/Current/General-Catalog/Courses") #displays every reviewed game on steam, 20 per page
    parsed = HTMLParser(src)
    div = parsed.css_first('[class=sc-child-item-links]')
    for node in div.css('a'): #game per page
        att = node.attrs
        href = att['href'] #gets link to sub-division course list
        sub=HTMLParser(gettext("https://catalog.ucsc.edu"+href))
        div2 = sub.css_first('[class=courselist]')
        div=''
        num=''
        title=''
        desc=''
        inst=''
        quarter=''
        tag=div2.css_first('h2')
        print(tag.next)
        while tag is not None:
            print("text=" +tag.text())
            att=tag.attrs
            try:
                c=att['class']
            except:
                csv.write(div + ',.' + num + ',.' + title + ',.' + desc + ',.' + inst + ',.' + quarter + '\n')
                break
            if c == 'course-name':
                if title:
                    csv.write(div + ',.' + num + ',.' + title + ',.' + desc + ',.' + inst + ',.' + quarter + '\n')
                    div=''
                    num=''
                    title=''
                    desc=''
                    inst=''
                #print(tag.text())
                ttext=tag.text().strip().split(' ')
                div, num = ttext[:2]
                print('div='+div)
                print('num='+num)
                title=' '.join(ttext[2:])
                print('title='+title)
            elif c == 'desc' and not desc:
                desc=tag.text().strip()
                print('desc='+desc)
            elif c == 'instructor':
                inst=tag.css_first('p').text().strip()
                print('inst='+inst)
            elif c == 'quarter':
                quarter=tag.css_first('p').text().strip()
                print('quarter='+quarter)
            tag=tag.next
    csv.close()
    return


def gettext(url):
    with requests.Session() as session:
        content = session.get(url).text
    return content


if __name__ == '__main__':
    main()
