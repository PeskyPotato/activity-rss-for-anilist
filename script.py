import requests
import os
from jinja2 import Environment, FileSystemLoader
import datetime

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))

username = os.getenv('USERNAME', '')
link = os.getenv('LINK', '')

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


def listActivity(userId):
    query = '''
    query ($userId: Int) {
      Page(page: 1, perPage:10) {
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
        'userId': userId
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    return (response.json())


def generate_feeds(userActivity):
    media_title = 'romaji'
    activities = []
    for activity in userActivity['data']['Page']['activities']:
        if not activity.get('progress'):
            title = f"{username} {activity.get('status')} {activity['media']['title'].get(media_title)}"
        else:
            title = f"{username} {activity.get('status')} {activity.get('progress')} of {activity['media']['title'].get('romaji')}"
        item = {
            'title': title,
            'pubDate': datetime.datetime.fromtimestamp(activity.get('createdAt')).strftime("%a, %d %b %Y %H:%M:%S +0000"),
            'url': activity.get('siteUrl')
        }
        activities.append(item)

    template = env.get_template("rss.xml")
    filename = f"activity-10-{media_title}.xml"
    filename_dir = os.path.join(root, 'feeds', filename)
    os.makedirs(os.path.dirname(filename_dir), exist_ok=True)
    print(link, filename)
    with open(filename_dir, "w") as fh:
        fh.write(template.render(
            title=f"{username}'s AniList User Activity",
            link=link,
            link_rss=link+filename,
            description=f"The unofficial AniList user activity feed for {username}.",
            language="en-gb",
            lastBuildDate=datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000"),
            items=activities
        ))


r = getUserID(username)
userId = r.get('data').get('User').get('id')
userActivity = listActivity(userId)
generate_feeds(userActivity)
