import requests
import math
import pandas as pd
from selectolax.parser import HTMLParser


#a scraper to get info from every class at UCSC
def main():
    #
    csv = open("db.csv",'a')
    #csv column names
    csv.write('course_division,course_number,course_title,description,instructors,quarters\n')
    
    #course catalog home page 
    src = gettext("https://catalog.ucsc.edu/Current/General-Catalog/Courses") 
    #get parser object
    parsed = HTMLParser(src)
    #get every course subject as a link
    div = parsed.css_first('[class=sc-child-item-links]')
    for node in div.css('a'): #for every course subject
        att = node.attrs
        href = att['href'] #gets link to sub-division course list
        sub=HTMLParser(gettext("https://catalog.ucsc.edu"+href)) #get parser object for course list
        div2 = sub.css_first('[class=courselist]')
        div=''
        num=''
        title=''
        desc=''
        inst=''
        quarter=''
        tag=div2.css_first('h2') #all class titles are under h2 
        print(tag.next)
        while tag is not None: #for every course under this subject
            #print("text=" +tag.text())
            att=tag.attrs
            
            try:
                c=att['class']
            except:
                csv.write(div + ',.' + num + ',.' + title + ',.' + desc + ',.' + inst + ',.' + quarter + '\n')
                break
            if c == 'course-name':
                #previous row has been filled. write that row to the csv.
                if title:
                    csv.write(div + ',.' + num + ',.' + title + ',.' + desc + ',.' + inst + ',.' + quarter + '\n')
                    div=''
                    num=''
                    title=''
                    desc=''
                    inst=''
                #get class subject, title, and number from this div's text
                ttext=tag.text().strip().split(' ')
                div, num = ttext[:2]
                print('div='+div)
                print('num='+num)
                title=' '.join(ttext[2:])
                print('title='+title)
            elif c == 'desc' and not desc:
                #get class description from text
                desc=tag.text().strip()
                print('desc='+desc)
            elif c == 'instructor':
                #get instructor list
                inst=tag.css_first('p').text().strip()
                print('inst='+inst)
            elif c == 'quarter':
                #get quarter list
                quarter=tag.css_first('p').text().strip()
                print('quarter='+quarter)
            tag=tag.next
    csv.close()
    return



#HTML GET requests the page
def gettext(url):
    with requests.Session() as session:
        content = session.get(url).text
    return content


if __name__ == '__main__':
    main()
