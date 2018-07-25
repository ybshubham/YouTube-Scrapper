import urllib
import MySQLdb
from bs4 import BeautifulSoup
import requests
import string
db = MySQLdb.connect(host="localhost",user="root",passwd="",db="onenightshot",use_unicode=True, charset="utf8")
cur = db.cursor()
v_id=list()
quries=[]
query=raw_input("enter searc topic")

base = 'https://www.youtube.com/results?search_query=' 

if query not in quries:
    quries.append(query)
    # Drop table if it already exist using execute() method.
    #cur.execute("DROP TABLE IF EXISTS "+query)
    url=base + "quantitative aptitube problems on" + query
    nquery=query.replace(" ","_")
    print query
    print nquery
    cur.execute("""CREATE TABLE """+nquery+""" (video_id  VARCHAR(20) UNIQUE,title  VARCHAR(100),publisher VARCHAR(50),  description VARCHAR(700),lengthv VARCHAR(100),views VARCHAR(10))""")
    
    r=requests.get(url)
    soup=BeautifulSoup(r.content)

    #scrapping first page
    s = soup.find_all('div',class_='yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix')

    for k in s:
        s1= k.contents[0]
        idv= k.get("data-context-item-id")
        video_id= idv
        v_id.append(video_id)
        #getting video_time
        vt=k.find('span',class_='video-time')
        video_tim= vt.text
    
        #getting video title
        vtt = k.find('h3',class_='yt-lockup-title ')
        vti=vtt.find('a')
        video_title= vti.get('title') 
    
        #getting video description
        desc = k.find('div',class_='yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2')
        video_description= desc.text
    
        #getting video channel
        ch = k.find('div',class_='yt-lockup-byline ')
        channel=ch.find('a')
        video_channel_name=channel.text
    
        #getting views
        vi=k.find('ul',class_='yt-lockup-meta-info')
    
        vti=vi.find_all('li')
        for i in vti:
            if "views" in i.text:
                views=i.text
        cur.execute("""INSERT INTO """+nquery+""" VALUES (%s,%s,%s,%s,%s,%s)""",(video_id,video_title,video_channel_name,video_description,video_tim,views))
        db.commit()

    #next pages scrapping starts here

    next_link=soup.find_all('a')
    for n in next_link:
        u=n.get('href')
        if "sp=S" in u:
            next_page_link= u
            for nextl in next_page_link:
                url='https://www.youtube.com'+next_page_link
                r=requests.get(url)
                soup=BeautifulSoup(r.content)
                s = soup.find_all('div',class_='yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix')

                for k in s:
                    s1= k.contents[0]
                    idv= k.get("data-context-item-id")
                    video_id= idv
                    if video_id not in v_id and video_id != '_tKwzsCL32I':
                        v_id.append(video_id)
                        print video_id
                        #getting video_time
                        vt=k.find('span',class_='video-time')
                        video_tim= vt.text
                
                        #getting video title
                        vtt = k.find('h3',class_='yt-lockup-title ')
                        vti=vtt.find('a')
                        video_title= vti.get('title') 
                
                        #getting video description
                        desc = k.find('div',class_='yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2')
                        video_description= desc.text  
                
                        #getting video channel
                        ch = k.find('div',class_='yt-lockup-byline ')
                        channel=ch.find('a')
                        video_channel_name=channel.text
                
                        #getting views
                        vi=k.find('ul',class_='yt-lockup-meta-info')
    
                        vti=vi.find_all('li')
                        for i in vti:
                            if "views" in i.text:
                                views=i.text
                        cur.execute("""INSERT INTO """+nquery+""" VALUES (%s,%s,%s,%s,%s,%s)""",(video_id,video_title,video_channel_name,video_description,video_tim,views))
          db.commit() 
