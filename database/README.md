This CSV database holds the info of every class at UCSC. the info for each class is separated as follows:
[Subject, Class number, Class name, Class description, Instructors, Quarters offered]

I used selectolax as my Html parsing library rather than BeautifulSoup for better scraping performance. 
The script starts from the course homepage, then scrapes all classes from each subject at a time.
