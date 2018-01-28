import json
import urllib.parse
import urllib.request
import csv
import sys

def get_coordinate_info(in_place):

    BASEURL='https://map.yahooapis.jp/geocode/V1/geoCoder?'
    place=urllib.parse.quote_plus(in_place,encoding='utf-8')
    PARAM='&query='+place+'&output=json&category=landmark'
    TOKEN='appid=dj0zaiZpPU8wNGRGdXJQTHVMbCZzPWNvbnN1bWVyc2VjcmV0Jng9ZDc-'

    URL=BASEURL+TOKEN+PARAM

    response=urllib.request.urlopen(URL)
    response_str=json.loads(response.read())
    return response_str

def output_csv(in_line_name,in_place_name,in_places,in_dir_path):
    if(in_places['ResultInfo']['Status']==200 and in_places['ResultInfo']['Count']>0):
        TAGS='Feature'
        in_dir_path.write(in_line_name+',')
        in_dir_path.write(in_place_name+',')
        in_dir_path.write(in_places[TAGS][0]['Geometry']['Coordinates']+'\n')

def print_error(in_str):
    error_msg=''
    if (in_str=='USAGE'):
        error_msg='ERROR IN USAGE: get_coornidate_info.py {MODE} {INPUT_PATH} {OUTPUT_PATH}\n \
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
            coordinate_info=get_coordinate_info(place[1])
            output_csv(place[0],place[1],coordinate_info,f_out)
        f_in.close()
        f_out.close()
    else:
        print_error("USAGE")
