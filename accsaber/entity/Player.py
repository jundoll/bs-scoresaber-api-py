# load modules
import os
from dataclasses import dataclass
from typing import Union

import requests
from bs4 import BeautifulSoup

# const
if 'USER_AGENT' in os.environ.keys():
    USER_AGENT = os.environ['USER_AGENT'].encode()
else:
    USER_AGENT = ''


# definition class
@dataclass(frozen=True)
class Player:

    playerId: str
    avatarUrl: str
    playerName: str
    rank: float
    ap: float
    hmd: Union[str, None]
    rankedPlays: float
    averageAcc: Union[float, None]
    averageApPerMap: Union[float, None]


# definition function
def gen(response):

    if response is not None:
        instance = Player(
            playerId=response.get('playerId'),
            avatarUrl=response.get('avatarUrl'),
            playerName=response.get('playerName'),
            rank=response.get('rank'),
            ap=response.get('ap'),
            hmd=response.get('hmd'),
            rankedPlays=response.get('rankedPlays'),
            averageAcc=response.get('averageAcc'),
            averageApPerMap=response.get('averageApPerMap')
        )
        return instance


def genList(response):

    if response is None:
        return None
    else:
        if type(response) is list:
            if len(response) == 0:
                return []
            else:
                return [gen(v) for v in response]
        elif type(response) is dict:
            return [gen(response)]


def fetch(soup):

    if soup is not None:
        # playerId
        elems = soup.select('div.hidden.md\:flex > div > a')
        playerId = elems[0].attrs['href'].split('/')[-1]

        # avatarUrl
        elems = soup.select('picture > img')
        avatarUrl = elems[0].attrs['src']

        # playerName
        elems = soup.select('h1 > div > span')
        playerName = elems[0].contents[0]

        # rank
        elems = soup.select('div:nth-child(1) > div > div:nth-child(1) > a')
        rank = int(elems[1].contents[2])

        # ap
        elems = soup.select(
            'div.flex.flex-col.justify-center.flex-1 > div:nth-child(2)')
        ap = float(elems[0].contents[0].replace(',', ''))

        # hmd
        elems = soup.select(
            'div.flex.flex-col.justify-center.flex-1 > div:nth-child(4)')
        hmd = elems[0].contents[0]

        # rankedPlays
        elems = soup.select(
            'div.flex.flex-col.justify-center.flex-1 > div:nth-child(3)')
        rankedPlays = int(elems[0].contents[0])

        # averageAcc
        averageAcc = None

        # averageApPerMap
        averageApPerMap = None

        # return
        instance = Player(
            playerId=playerId,
            avatarUrl=avatarUrl,
            playerName=playerName,
            rank=rank,
            rankedPlays=rankedPlays,
            hmd=hmd,
            ap=ap,
            averageAcc=averageAcc,
            averageApPerMap=averageApPerMap
        )
        return instance


def fetchList(soup, url):

    if soup is not None:
        # init
        instances = []

        # the number of pages
        elems = soup.select('main > form:nth-child(1) > div:nth-child(2)')
        max_pages = int(elems[0].contents[-1])

        # loop for page
        for page in range(max_pages):

            # page 2 ~
            if page > 0:
                request_url = f'{url}?page={page+1}'
                response = requests.get(request_url, headers={
                                        "User-Agent": USER_AGENT})
                soup = BeautifulSoup(response.content, "html.parser")

            num4page = len(soup.select('table > tbody > tr'))
            for i in range(num4page):

                # playerId
                elems = soup.select(
                    f'table > tbody > tr:nth-child({i+1}) > td:nth-child(3) > a')
                playerId = elems[0].attrs['href'].split('/')[-3]

                # avatarUrl
                elems = soup.select(
                    f'table > tbody > tr:nth-child({i+1}) > td.relative.w-10.aspect-square > picture > img')
                avatarUrl = elems[0].attrs['src']

                # playerName
                elems = soup.select(
                    f'table > tbody > tr:nth-child({i+1}) > td:nth-child(3) > a')
                playerName = str(elems[0].contents[0])

                # rank
                elems = soup.select(
                    f'table > tbody > tr:nth-child({i+1}) > td:nth-child(1)')
                rank = int(elems[0].contents[-1])

                # ap
                elems = soup.select(
                    f'table > tbody > tr:nth-child({i+1}) > td:nth-child(4)')
                ap = float(elems[0].contents[0].replace(',', ''))

                # hmd
                elems = soup.select(
                    f'table > tbody > tr:nth-child({i+1}) > td:nth-child(8)')
                if len(elems[0].contents) > 0:
                    hmd = str(elems[0].contents[0])
                else:
                    hmd = None

                # rankedPlays
                elems = soup.select(
                    f'table > tbody > tr:nth-child({i+1}) > td:nth-child(6)')
                rankedPlays = int(elems[0].contents[0])

                # averageAcc
                elems = soup.select(
                    f'table > tbody > tr:nth-child({i+1}) > td:nth-child(5)')
                averageAcc = float(elems[0].contents[0].replace(',', ''))

                # averageApPerMap
                elems = soup.select(
                    f'table > tbody > tr:nth-child({i+1}) > td:nth-child(7)')
                averageApPerMap = float(elems[0].contents[0].replace(',', ''))

                # add
                instance = Player(
                    playerId=playerId,
                    avatarUrl=avatarUrl,
                    playerName=playerName,
                    rank=rank,
                    rankedPlays=rankedPlays,
                    hmd=hmd,
                    ap=ap,
                    averageAcc=averageAcc,
                    averageApPerMap=averageApPerMap
                )
                instances += [instance]

        # return
        return instances
