import praw
import argparse


def parse_args():
    # build the command line parser
    parser = argparse.ArgumentParser(description='get the top 10 posts from the previous week')
    parser.add_argument('subreddit_name',
                        help='subreddit to pull the top 10 posts',
                        action='store')
    return parser.parse_args()


args = parse_args()


# get the top 10 posts from the previous week

# TODO - create your own app string for curator

# TODO - what kind of tests can you add?

# TODO - what if the number of posts is less than 10?

# TODO - what if reddit is experiencing a network issue?

# TODO - use command line argument to specify the subreddit

subreddit_name = args.subreddit_name
reddit = praw.Reddit('pycomic')
subreddit = reddit.subreddit(subreddit_name)

print(f'\nTop 10 posts of the week for the {subreddit_name} subreddit')
print('-' * 80)
print()
for submission in subreddit.top('week', limit=10):
    print(f'{submission.title} - {submission.url}')
