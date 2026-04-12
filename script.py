import requests
import os
from jinja2 import Environment, FileSystemLoader
import datetime
import argparse
import rss_py

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))

url = 'https://graphql.anilist.co'


def getUserID(name):
    query = '''
    query ($name: String) {
      User (name: $name) {
        id
      }
    }
    '''

    variables = {
        'name': name
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    return (response.json())


def listActivity(userId, perPage):
    query = '''
    query ($userId: Int, $perPage: Int) {
      Page(page: 1, perPage:$perPage) {
        activities(userId: $userId, sort: ID_DESC) {
          ... on ListActivity {
            type
            createdAt
            progress
            status
            media {
              title {
                romaji
                english
                native
              }
            }
            siteUrl
          }
        }
      }
    }
    '''

    variables = {
        'userId': userId,
        'perPage': perPage
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    return (response.json())


def generate_feeds(username, link, userActivity, perPage, output):
    media_title = 'romaji'
    activities = []
    for activity in userActivity['data']['Page']['activities']:
        if not activity.get('progress'):
            title = f"{username} {activity.get('status')} {activity['media']['title'].get(media_title)}"
        else:
            title = f"{username} {activity.get('status')} {activity.get('progress')} of {activity['media']['title'].get('romaji')}"
        item = rss_py.Item(
            title=title,
            pubDate=datetime.datetime.fromtimestamp(activity.get('createdAt'), tz=datetime.timezone.utc),
            link=activity.get('siteUrl')
        )
        activities.append(item)

    filename = f"anilist-{perPage}-{media_title}.xml"
    filename_dir = os.path.join(root, 'feeds', filename)
    if output:
      filename_dir = os.path.join(
         os.path.abspath(output), filename
      )
    os.makedirs(os.path.dirname(filename_dir), exist_ok=True)
    print(link, filename)
    with open(filename_dir, "w") as fh:
        feed = rss_py.Channel(
            title=f"{username}'s AniList User Activity",
            link=link,
            description=f"The unofficial AniList user activity feed for {username}.",
            language="en-gb",
            lastBuildDate=datetime.datetime.now(datetime.timezone.utc),
            atomSelfLink=f"{link}{filename}",
            items=activities
        )
        fh.write(rss_py.build(feed))


def cli_entry():
  parser = argparse.ArgumentParser()
  parser.add_argument("--username",
                      default=os.getenv('USERNAME', ''),
                      help="Anilist username")
  parser.add_argument("--link", default=os.getenv('LINK', ''),
                      help="Link to use for the RSS feed channel")
  parser.add_argument("--per-page", default=os.getenv('PER_PAGE', ''),
                      type=int,
                      help="Maximum items to include in the RSS feed")
  parser.add_argument("--output", help="Ouput directory of the RSS feed")

  args = parser.parse_args()
  main(args.username, args.link, args.per_page, args.output)

def main(username=None, link=None, perPage=None, output=None):
  r = getUserID(username)
  userId = r.get('data').get('User').get('id')
  userActivity = listActivity(userId, perPage)
  generate_feeds(username, link, userActivity, perPage, output)

if __name__ == "__main__":
    cli_entry()
