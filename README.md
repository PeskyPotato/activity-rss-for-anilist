# Activity RSS for AniList

> Generate an rss feed for an AniList users activity.

This is an unofficial Python script that uses the public [AniList API](https://anilist.gitbook.io/anilist-apiv2-docs) to generate an RSS feed for a users anime and manga activity.

Below is an abridged example of file that the script generates for the AniList user PeskyPotato. The full live file can be found [on my website.](https://pesky.moe/feeds/anilist-10-romaji.xml)

```xml
<rss version="2.0">
	<channel>
		<title>PeskyPotato's AniList User Activity</title>
		<link>https://pesky.moe/feeds/</link>
		<description>The unofficial AniList user activity feed for PeskyPotato.</description>
		<language>en-gb</language>
		<atom:link href="https://pesky.moe/feeds/anilist-10-romaji.xml" rel="self" type="application/rss+xml"/>
		<lastBuildDate>Sun, 16 Jun 2024 11:33:11 +0000</lastBuildDate>
		<item>
			<title>PeskyPotato completed Dungeon Meshi</title>
			<link>https://anilist.co/activity/744756742</link>
			<pubDate>Fri, 14 Jun 2024 05:56:21 +0000</pubDate>
			<guid>https://anilist.co/activity/744756742</guid>
		</item>
	</channel>
</rss>
```

The repository also contains a GitHub Action workflow that will generate the file on each push and daily at 08:00UTC. The workflow also deploys the file via SSH to a remote host. This is currently what I use to host my file, but can be omitted or modified to your use. The Python script can work on it's own to generate the RSS file.

## Installation
The script requires Python 3. Using pip install the dependencies:
```
pip install -r requirements.txt
```

## Usage
Set the username and and URL to the website for the feed as environment variables. On Linux or macOS this can be done like so:
```bash
export USERNAME=PeskyPotato
export LINK=https://pesky.moe/feeds/
```

Run the script:
```
python script.py
```

The XML file will be created in the `feeds/` directory. It will contain the 10 latest activities using the medias romaji title.

## License
MIT