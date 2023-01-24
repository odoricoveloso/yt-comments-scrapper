from youtube_comment_downloader import *
import pandas as pd
import logging
import os
from datetime import datetime
import pytz
from pytz import timezone

filename = 'video_ids.csv'  # CHANGE THIS VALUE WITH LIST OF IDS

# datetime config
datetimesp = datetime.now(pytz.timezone('America/Sao_Paulo'))
dt = datetimesp.strftime('%d/%m/%Y %H:%M')
tz = timezone('America/Sao_Paulo')
def timetz(*args):
	return datetime.now(tz).timetuple()

# logging config
logging.Formatter.converter = timetz
logging.basicConfig(filename = 'comments.log', filemode = 'w', level = logging.INFO, format = '%(asctime)s | %(message)s', datefmt='%Y/%m/%d %H:%M:%S %Z', force = True)

# function to get comments
def getComments(videoid):

	# check if comments file already exists
	writefilename = 'comments/' + videoid + '.xlsx'
	if os.path.isfile(writefilename):
		message = 'comments file already exists'
		return message
	
	downloader = YoutubeCommentDownloader()
	
    # get comments
	try:
		start_time = time.time()
		print('Downloading comments for ' + videoid)
		comments = downloader.get_comments(videoid)
	except:
		message = 'Cannot get comments.'
		return message

    # create dataFrame and save to excel file
	try:
		df = pd.DataFrame(comments)
		count = len(df.index)
		df.to_excel('comments/' + videoid + '.xlsx', index=False)
	except:
		message = 'Cannot save to dataFrame.'
		return message

	message = 'Downloaded ' + str(count) + ' comments in [{:.2f} seconds]. Done!'.format(time.time() - start_time)
	return message

# read CSV file
dados = pd.read_csv(filename)

# call function
for i, id in enumerate(dados['videoId']):
	videoid = dados.loc[i, 'videoId']
	message = getComments(videoid)
	logging.info(f'{str(i)} | {videoid} | {message}')
	print(dt + " | " + str(i) + " | " + videoid + " | " + message)