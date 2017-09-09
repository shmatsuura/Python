import json
import urllib.parse
import urllib.request
import csv
import datetime
import os.path
import sys
import pandas 
import numpy

def get_train_info():

    BASEURL='https://api.tokyometroapp.jp/api/v2/datapoints?'
    PARAM='rdf:type=odpt:Train&acl:consumerKey='
    TOKEN='15131163ebf8888e03160d19740103af9ec771067ff295ef44a6f032ddf8c821'

    URL=BASEURL+PARAM+TOKEN

    response=urllib.request.urlopen(URL)
    response_str=json.loads(response.read())
    return response_str

def output_csv(in_train_info,in_dir_path):

    RAILWAY='odpt:railway'
    TRAINNUM='odpt:trainNumber'
    DELAY='odpt:delay'
    TRAINOWNER='odpt:trainOwner'

    RAILWAY_TO_REMOVE='odpt.Railway:TokyoMetro.'
    TRAINOWNER_TO_REMOVE='odpt.TrainOwner:.'
    RAIWALY_TO_REMOVE_LEN=len(RAILWAY_TO_REMOVE)
    TRAINOWNER_TO_REMOVE_LEN=len(TRAINOWNER_TO_REMOVE)

    date=datetime.datetime.now()
    date_str=date.strftime('%Y-%m-%d')
    FILE_NAME=in_dir_path+'train_info_'+date_str+'.csv'

    if (os.path.isdir(in_dir_path)==False):
        print_error('DIR')
    else:
        f=open(FILE_NAME, "a+")
        if os.path.getsize(FILE_NAME)==0:
            f.write('line,')
            f.write('train_num,')
            f.write('delay,')
            f.write('trainowner\n')
        for train_info in in_train_info:
            railway_info=train_info[RAILWAY][RAIWALY_TO_REMOVE_LEN:]
            trainnum_info=train_info[TRAINNUM]
            delay_info=train_info[DELAY]
            trainowner_info=train_info[TRAINOWNER][TRAINOWNER_TO_REMOVE_LEN-1:]
            f.write(railway_info+',')
            f.write(trainnum_info+',')
            f.write(str(delay_info)+',')
            f.write(trainowner_info+'\n')
        f.close()    

def analyze_train_info(in_dir_path):
    train_info=pandas.read_csv(in_dir_path)
    # 1. NUMBER OF TRAIN OPERATIONS BY EACH LINE
    train_info_unique=train_info.drop_duplicates(subset=['train_num'])
    line_num=train_info_unique.groupby('line').count()
    line_num_sorted=line_num.sort_values(by=['train_num'],ascending=False)
    print('### 1. NUMBER OF TRAIN OPERATIONS BY EARCH LINE ###')
    print(line_num_sorted['train_num'])

    # 2. NUMBER OF TRAIN OPERATORS
    train_info_unique=train_info.drop_duplicates(subset=['train_num'])
    owner_num=train_info_unique.groupby('trainowner').count()
    owner_num_sorted=owner_num.sort_values(by=['train_num'],ascending=False)
    print('### 2. NUMBER OF TRAIN OWNER IN TOKYO METRO ###')
    print(owner_num['train_num'])
    return 

def print_error(in_str):
    error_msg=''
    if (in_str=='USAGE'):
        error_msg='ERROR IN USAGE: get_train_info.py {MODE} {PATH}\n \
                     {MODE}: g to collect train info \
                             a to analyze train info'
    if (in_str=='DIR'):
        error_msg='DIRECTORY DOES NOT EXISTS.'+'in_dir'
    print(error_msg)
    sys.exit(1)

if __name__=='__main__':
    argv=sys.argv
    argc=len(argv)
    if (argc<3):
        print_error("USAGE")
    if(argv[1]=='g'):
        dir_path=argv[2]
        train_info=get_train_info()
        output_csv(train_info,dir_path)
    if(argv[1]=='a'):
        dir_path=argv[2]
        analyze_train_info(dir_path)
