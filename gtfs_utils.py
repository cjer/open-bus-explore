import pandas as pd
from ftplib import FTP
import datetime
import re
import zipfile
import os

MOT_FTP = 'gtfs.mot.gov.il'
FILE_NAME = 'israel-public-transportation.zip'
LOCAL_ZIP_PATH = 'data/sample/gtfs.zip' 
TEMP_LOCAL_PATH = 'data/sample/gtfs_temp.zip'
TARIFF_TXT_NAME = 'Tariff.txt'

def ftp_connect():
	conn = FTP(MOT_FTP)
	conn.login()
	return conn

def get_ftp_dir(conn):
	ftp_dir = []
	conn.retrlines('LIST', lambda x: ftp_dir.append(x)) 
	return ftp_dir

def get_uptodateness(ftp_dir, file_name = FILE_NAME, local_zip_path = LOCAL_ZIP_PATH):
	RE_FTP_LINE = re.compile(
	    r'(?P<date>\d+-\d+-\d+\s+\d+:\d+[APM]{2})\s+(?P<size><DIR>|[0-9]+)\s+(?P<file_name>.*)')
	f = [re.findall(RE_FTP_LINE, line) for line in ftp_dir]
	f_dates = {t[0][2]: datetime.datetime.strptime(t[0][0], "%m-%d-%y  %H:%M%p") for t in f}

	ftp_date = f_dates[file_name]

	our_date = datetime.datetime.fromtimestamp(os.path.getmtime(local_zip_path))
	return  (ftp_date - our_date).days

def get_ftp_file(conn, file_name = FILE_NAME, local_zip_path = LOCAL_ZIP_PATH ):
	temp_local_path = local_zip_path+'_temp'
	fh = open(temp_local_path, 'wb')
	conn.retrbinary('RETR %s' % (file_name), fh.write)
	fh.close()
	os.remove(local_zip_path)
	os.rename(temp_local_path, local_zip_path)



def extract_tariff_df(local_zip_path, tariff_txt_name = TARIFF_TXT_NAME):
	cols = ['ShareCode','ShareCodeDesc','ZoneCodes','Daily','Weekly','Monthly','FromDate','ToDate', 'EXTRA']
	with zipfile.ZipFile(local_zip_path) as zf:
	    tariff_df = (pd.read_csv(zf.open(tariff_txt_name), header=None, skiprows=[0], names = cols)
	    .drop(columns = ['EXTRA']))
	# remove ShareCodes which contain multiple zones  e.g. גוש דן מורחב
	tariff_df = (tariff_df[~ tariff_df.ZoneCodes.str.contains(';')]
	             .rename(columns = {'ShareCodeDesc': 'zone_name',
	                               'ZoneCodes': 'zone_id'}))
	return tariff_df