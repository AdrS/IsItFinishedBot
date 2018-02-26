from slackclient import SlackClient
import os

#TODO: we could cache things like user and channel lists
sc = None

def just_one(items):
	'returns the only item in the list if the list has exactly one element'
	if len(items) == 1:
		return items[0]

def get_members_list():
	reply = sc.api_call('users.list')
	if not reply['ok']: return
	return reply['members']

def get_user(username):
	members = get_members_list()
	if not members: return
	return just_one([m for m in members if m['name'] == username])

def get_user_id(username):
	user = get_user(username)
	if not user: return
	return user['id']

def get_user_dm_channel(username):
	user_id = get_user_id(username)
	# Could not get user id
	if not user_id: return

	# Get list of im channels
	reply = sc.api_call('im.list')
	if not reply['ok']: return
	return just_one([im for im in reply['ims'] if im['user'] == user_id])

def get_dm_id(username):
	dm = get_user_dm_channel(username)
	if not dm: return
	return dm['id']

def get_channel(channel_name):
	reply = sc.api_call('channels.list')
	if not reply['ok']: return
	return just_one([c for c in reply['channels'] if c['name'] == channel_name])

def get_channel_id(channel_name):
	channel = get_channel(channel_name)
	if not channel: return
	return channel['id']

def dm_user(username, message):
	dm_channel_id = get_dm_id(username)
	if not dm_channel_id: return
	reply = sc.api_call('chat.postMessage',channel=dm_channel_id, text=message)
	return reply

def post_message(message, channel_ids):
	replies = []
	for c in channel_ids:
		reply = sc.api_call('chat.postMessage',channel=c, text=message)
		replies.append(reply)
	return replies

def post_file(filename, channel_ids):
	# Slack limits files to 1mb
	max_size = (1<<20)
	initial_comment = ''
	try:
		with open(filename, 'r') as f:
			content = f.read(max_size)
			if os.fstat(f.fileno()).st_size > max_size:
				initial_comment = 'Warning: file was truncated to limit size to 1mb'
	except Exception as e:
		content = str(e)
		initial_comment = content

	reply = sc.api_call('files.upload',
					channels=channel_ids,
					filename=filename,
					content=content,
					initial_comment=initial_comment)
	return reply
