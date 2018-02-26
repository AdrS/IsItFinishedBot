# IsItFinishedBot
A utility for posting messages to slack when a shell command finishes

# Examples
- Send a message to a user

  ```./iifb.py -u adrs -m "hello"```
- Send a file to a user

  ```./iifb.py -u adrs setup.txt```
- Tell user when a long running command finishes

  ```./iifb.py -u adrs -s "curl http://example.com/large_file -o file"```

- Run command and upload output to slack

  ```./iifb.py -u adrs -s "ls -l > tmp.txt" tmp.txt```
  ![What results look like in slack](https://github.com/AdrS/IsItFinishedBot/blob/master/images/example.png)

# Usage
```
Usage: iifb.py [options] [files]

A utility for running scripts and posting the results to slack.

If a shell command is specified, the shell command is run. The runtime and
return code are posted to slack along with any files and messages.

If a message is specified, the message is sent to specified user or channel.

The files specified do not need to exist. (ex: They could be logs generated
by the shell command)

By default, an authentication token is read from "~/.iifb.json". To
override this behavior, user the -t <token> option.


Options:
  -h, --help            show this help message and exit
  -u USER, --user=USER  User to send direct message to
  -c CHANNEL, --channel=CHANNEL
                        Channel to post message to
  -m MESSAGE, --message=MESSAGE
                        Message to post
  -s SHELL_COMMAND, --shell-command=SHELL_COMMAND
                        Shell command to run
  -t TOKEN, --token=TOKEN
                        Authentication token
```

# Warnings
Slack limits file uploads to 1mb. Files are automatically truncated to stay within these limits.
![Slack file limits](https://github.com/AdrS/IsItFinishedBot/blob/master/images/file_too_big.png)

# Credits
Duck logo is from [Wikipedia](https://commons.wikimedia.org/wiki/File:Creative-Tail-Animal-duck.svg) and is licensed under the Creative Commons.
