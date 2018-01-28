import json
import urllib.parse
import urllib.request
import csv
import sys

def get_weather_info(in_lat,in_long):

    BASEURL='https://map.yahooapis.jp/weather/V1/place?'

    PARAM='coordinates='+str(in_lat)+','+str(in_long)+'&output=json'
    TOKEN='&appid=dj0zaiZpPU8wNGRGdXJQTHVMbCZzPWNvbnN1bWVyc2VjcmV0Jng9ZDc-'

    URL=BASEURL+PARAM+TOKEN
    response=urllib.request.urlopen(URL)
    response_str=json.loads(response.read())
    return response_str

def output_csv(in_line_name,in_place_name,in_weather,in_dir_path):
    if(in_weather['ResultInfo']['Status']==200 and in_weather['ResultInfo']['Count']>0):
        TAGS='Feature'
        weather=in_weather[TAGS][0]['Property']['WeatherList']['Weather']['Type'=='observation']
        in_dir_path.write(in_line_name+',')
        in_dir_path.write(in_place_name+',')
        in_dir_path.write(weather['Date']+',')
        in_dir_path.write(str(weather['Rainfall'])+'\n')

def print_error(in_str):
    error_msg=''
    if (in_str=='USAGE'):
        error_msg='ERROR IN USAGE: get_weather_info.py {MODE} {INPUT_PATH} {OUTPUT_PATH}\n \
                     {MODE}: g to collect coordinate'
    print(error_msg)
    sys.exit(1)

if __name__=='__main__':
    argv=sys.argv
    argc=len(argv)
    if (argc<4):
        print_error("USAGE")
    if(argv[1]=='g'):
        input_dir_path=argv[2]
        output_dir_path=argv[3]
        f_in=open(input_dir_path, "r")
        f_out=open(output_dir_path,"a+")
        data=csv.reader(f_in)
        for place in data:
            weather_info=get_weather_info(place[2],place[3])
            output_csv(place[0],place[1],weather_info,f_out)
        f_in.close()
        f_out.close()
    else:
        print_error("USAGE")
