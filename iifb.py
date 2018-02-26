#!/usr/bin/python3

import json
import optparse
import os
import slack
import sys

#TODO: cache info for 24 hours

def load_config():
	with open(os.path.expanduser('~/.iifb.json'), 'r') as f:
		config = json.load(f)
		if 'Token' in config:
			return config['Token']


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
