import praw
import sqlite3
import time

USERAGENT = "/u/jaytongsays comment bot to help other redditors discover top songs of an artist submitted to a music subreddit"
USERNAME = "bopfm_bot"
PASSWORD = "s0undch3ck123"
SUBREDDIT = 'listentothis'
LIMIT = 10
KEYWORDS = [" -- "," - "]
WAIT = 600

print("logging in")
r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)


sql = sqlite3.connect('sql.db')
print('Loaded SQL Database')
cur = sql.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
print("Loaded Database")


def scan():
	print("starting scan")
	subreddit = r.get_subreddit(SUBREDDIT)
	for submission in subreddit.get_new(limit=LIMIT):
		cur.execute('SELECT * FROM oldposts WHERE ID=?', [submission.url])
		if not cur.fetchone():
			cur.execute('INSERT INTO oldposts VALUES(?)', [submission.url])
			title = submission.title.encode()
			for key in KEYWORDS:
			    if key in title:
			        print(title)
			        before, after = title.split(key)
			        print(before)
			        submission.add_comment("If you like this track, give OP an upvote and check out " + before + "'s other top songs: https://bop.fm/a/"+str.lower(before.replace(' ','-')))
	sql.commit()



while True:
	try:
		scan()
	except:
		print('Failed to scan')
	print('Waiting ' + str(WAIT) + ' seconds')
	time.sleep(WAIT)