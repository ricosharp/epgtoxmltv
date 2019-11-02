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
epg += '<channel id="%s">\n' % channel_id
epg += '\t<display-name>%s</display-name>\n' % channel_name
epg += '</channel>\n'

def format_time(current_program):
    datetime_start = datetime.datetime.strptime(response['Schedule']['Programs'][i]['TVGuideDateTime'] , '%d-%b-%Y %H:%M:%S')
    datetime_stop = datetime.datetime.strptime(response['Schedule']['Programs'][i + 1]['TVGuideDateTime'] , '%d-%b-%Y %H:%M:%S')
    prog_start = datetime_start.strftime('%Y%m%d%H%M%S')
    prog_end = datetime_stop.strftime('%Y%m%d%H%M%S')
    return prog_start, prog_end

for i in range(number_of_programs):
    program_title = response['Schedule']['Programs'][i]['SeriesTitle'].replace('&' , '&amp;')
    program_desc = response['Schedule']['Programs'][i]['Synopsis'].replace('&' , '&amp;')
    program_start, program_stop = format_time(i)
    epg += '<programme start="%s +0300" stop="%s +0300" channel="%s">\n' % (program_start, program_stop, channel_id)
    epg += '\t<title>%s</title>\n' % program_title
    epg += '\t<desc>%s</desc>\n' % program_desc
    epg += '</programme>\n'
epg += '</tv>'
xmltv_file = open(channel_id + '.xml' , 'w+')
xmltv_file.write(epg)