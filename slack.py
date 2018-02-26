from slackclient import SlackClient

#TODO: we could cache things like user and channel lists

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
	#TODO: add support for sending attachements
	dm_channel_id = get_dm_id(username)
	if not dm_channel_id: return
	reply = sc.api_call('chat.postMessage',channel=dm_channel_id, text=message)
	return reply
