import youtube_comment_downloader as ycd
import pandas as pd
import logging
import os
import time

script_path = os.path.dirname(os.path.abspath(__file__))
filename = f'{script_path}/ids_novos.csv'

# logging config
logging.basicConfig(filename = f'{script_path}/comments.log', filemode = 'w', level = logging.INFO, format = '%(asctime)s | %(message)s', datefmt='%Y/%m/%d %H:%M:%S %Z', force = True)

# function to get comments
def getComments(videoid):

	# check if comments file already exists
	writefilename = f'{script_path}/comments/' + videoid + '.json'
	if os.path.isfile(writefilename):
		message = 'comments file already exists'
		return message
	
	downloader = ycd.YoutubeCommentDownloader()
	
    # get comments
	try:
		start_time = time.time()
		print('Downloading comments for ' + videoid)
		comments = downloader.get_comments(videoid)
	except:
		message = 'Cannot get comments.'
		return message

    # create dataFrame and save to json file
	try:
		df = pd.DataFrame(comments)
		count = len(df.index)
		json_filename = f'{script_path}/comments/' + videoid + '.json'
  
		with open(json_filename, 'w', encoding='utf8') as f:
			f.write(df.to_json(orient='records', indent=4, force_ascii=False))
   
	except Exception as e:
		message = 'Cannot save to dataFrame. Error: ' + str(e)
		return message

	message = 'Downloaded ' + str(count) + ' comments in [{:.2f} seconds]. Done!'.format(time.time() - start_time)
	return message

# read CSV file
dados = pd.read_csv(filename, encoding='utf8')

# call function
for i, id in enumerate(dados['videoId']):
	videoid = dados.loc[i, 'videoId']
	message = getComments(videoid)
	logging.info(f'{str(i)} | {videoid} | {message}')
	print(str(i) + " | " + videoid + " | " + message)
