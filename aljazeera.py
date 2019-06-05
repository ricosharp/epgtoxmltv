import requests
import datetime

# This will download EPG data from https://www.aljazeera.com/watch_now/epgschedule.html into JSON format
# It will then produce a file called tv.aljazeera.live.xml

today  = datetime.datetime.now().strftime('%d-%B-%Y')
data = 'Cmd=&StartDate=' + today + '&TimeZone=-4%3A00%3A00&ProdPreview=true'
response = requests.post('https://www.aljazeera.com/addons/Schedule.ashx', data=data).json()

number_of_programs = len(response['Schedule']['Programs']) - 1

channel_id = "tv.aljazeera.live"
channel_name = "Al Jazeera"

epg = '<tv>\n'
epg += '<channel id="' + channel_id + '">\n'
epg += '\t<display-name>' + channel_name + '</display-name>\n'
epg += '</channel>\n'
for i in range(number_of_programs):
    program_title = response['Schedule']['Programs'][i]['SeriesTitle'].replace('&' , '&amp;')
    program_desc = response['Schedule']['Programs'][i]['Synopsis'].replace('&' , '&amp;')
    tvg_datetime_start = datetime.datetime.strptime(response['Schedule']['Programs'][i]['TVGuideDateTime'] , '%d-%b-%Y %H:%M:%S')
    tvg_datetime_stop = datetime.datetime.strptime(response['Schedule']['Programs'][i + 1]['TVGuideDateTime'] , '%d-%b-%Y %H:%M:%S')
    program_start = tvg_datetime_start.strftime('%Y%m%d%H%M%S') 
    program_stop = tvg_datetime_stop.strftime('%Y%m%d%H%M%S')
    epg += tvg_datetime_start.strftime('%Y\n')
    epg += '<programme start="' + program_start + ' +0300' '" stop="' + program_stop + ' +0300' '" channel="' + channel_id + '">\n'
    epg += '\t<title>' + program_title + '</title>\n'
    epg += '\t<desc>' + program_desc + '</desc>\n'
    epg += '</programme>\n'
epg += '</tv>'

xmltv_file = open(channel_id + '.xml' , 'w+')
xmltv_file.write(epg)