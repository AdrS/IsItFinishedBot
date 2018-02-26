#!/usr/bin/python3

from datetime import datetime
import json
import optparse
import os
import slack
import subprocess
import sys

#TODO: cache info for 24 hours

def load_config():
	with open(os.path.expanduser('~/.iifb.json'), 'r') as f:
		config = json.load(f)
		if 'Token' in config:
			return config['Token']

def get_channel_ids(user, channel):
	# Get ids of channels to post to
	channel_ids = []
	if user:
		uid = slack.get_dm_id(options.user)
		if not uid:
			print('error: could not get user id')
		else:
			channel_ids.append(uid)
	if options.channel:
		cid = slack.get_channel_id(options.channel)
		if not cid:
			print('error: could not get channel id')
		else:
			channel_ids.append(uid)

	if not channel_ids:
		print('error: could not get any channel ids to sent to')
		sys.exit(1)
	return channel_ids

if __name__ == '__main__':
	parser = optparse.OptionParser('''usage: %prog [options] [files]
A utility for running scripts and posting the results to slack.

If a shell command is specified, the shell command is run. The runtime and
return code are posted to slack along with any files and messages.

If a message is specified, the message is sent to specified user or channel.

The files specified do not need to exist. (ex: They could be logs generated
by the shell command)

By default, an authentication token is read from "~/.iifb.json". To
override this behavior, user the -t <token> option.
''')

	parser.add_option('-u', '--user', help='User to send direct message to')
	parser.add_option('-c', '--channel', help='Channel to post message to')
	parser.add_option('-m', '--message', help='Message to post')
	parser.add_option('-s', '--shell-command', help='Shell command to run')
	parser.add_option('-t', '--token', help='Authentication token')

	(options, files) = parser.parse_args()

	# Check arguments
	if not (options.user or options.channel):
		print('error: must specify a user to dm or a channel to post to')
		sys.exit(1)

	if not (options.message or files or options.shell_command):
		print('error: must specify a message or files to send or a shell command')
		sys.exit(1)

	token = options.token or load_config()
	slack.sc = slack.SlackClient(token)

	# Check that user/channel exists so we can fail early
	channel_ids = get_channel_ids(options.user, options.channel)
	assert(channel_ids)

	message = options.message or ''

	# Run shell command and keep track runtime + return code
	if options.shell_command:
		start_time = datetime.now()

		# Should I capture output?
		return_code = subprocess.call(options.shell_command, shell=True)

		runtime = datetime.now() - start_time
		message = '\n'.join([message,
					'Command: "%s"' % options.shell_command,
					'Runtime: %s' % runtime,
					'Status: %d' % return_code])

		# Get fresh channel ids if command took > 1hr to run
		if runtime.total_seconds() > 60*60:
			channel_ids = get_channel_ids(options.user, options.channel)

	if message:
		res = slack.post_message(message, channel_ids)
		#print(res)
		#TODO: check for errors

	for f in files:
		res = slack.post_file(f, channel_ids)
		if not res['ok']:
			print('error: could not post file', f)
