from .models import Episode, Show
from django.conf import settings
from . import extensions
import xml.dom.minidom


def rss_generate_for_episode(episode: Episode):
    return f"""
    <item>
            <author>{episode.show.user.first_name} {episode.show.user.last_name}</author>
            <itunes:author>{episode.show.user.first_name} {episode.show.user.last_name}</itunes:author>
            <title>{episode.title}</title>
            <pubDate>{extensions.correct_date(str(episode.pubDate))}</pubDate>
            <enclosure url="{episode.audio.url}" type="{episode.media_mime_type}" length="{episode.audio.size}" />
            <itunes:duration>{episode.duration}</itunes:duration>
            <guid isPermaLink="false">{episode.guid}</guid>
            <itunes:explicit>{"yes" if episode.explicit else "no"}</itunes:explicit>
            <description>
                {episode.description}
            </description>
    </item>
    """

def rss_generate_for_show(show: Show, episodes: [Episode]): # type: ignore
    my_channel_rss = f"""<?xml version="1.0" encoding="windows-1254"?>
    <rss xmlns:googleplay="http://www.google.com/schemas/play-podcasts/1.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:rawvoice="http://www.rawvoice.com/rawvoiceRssModule/" xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">

    <channel>
    <title>{show.title}</title>
        <googleplay:author>{show.user.first_name} {show.user.last_name}</googleplay:author>
        <author>{show.user.first_name} {show.user.last_name}</author>
        <itunes:author>{show.user.first_name} {show.user.last_name}</itunes:author>
        <itunes:email>{show.user.email}</itunes:email>
        <itunes:owner>
        <itunes:name>{show.user.first_name} {show.user.last_name}</itunes:name>
        <itunes:email>{show.user.email}</itunes:email>
        </itunes:owner>
        <itunes:category text="{show.category}" />
        <image>
        <url>{show.cover.url}</url>
        <title>{show.title}</title>
        <link>/shows/rss/{show.id}</link>
        </image>
       
        <itunes:keywords>{show.keywords}</itunes:keywords>
        <copyright>{show.copyright}</copyright>
        <description>{show.description}</description>
        <googleplay:image href="{show.cover.url}" />
        <language>{show.language}</language>
        <itunes:explicit>{"yes" if show.explicit else "no"}</itunes:explicit>
        <pubDate>{extensions.correct_date(str(show.pubDate))}</pubDate>
        <link>/shows/rss/{show.id}</link>
        <itunes:image href="{show.cover.url}" />

        {"".join([rss_generate_for_episode(ep) for ep in episodes])}
    </channel>
    </rss>
    """

    dom = xml.dom.minidom.parseString(my_channel_rss)
    return dom.toprettyxml()