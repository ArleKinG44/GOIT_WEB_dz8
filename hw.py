import redis

from redis_lru import RedisLRU
from models import Author, Quote


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    quotes =  Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[str | None]:
    authors =  Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes =  Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


if __name__ == '__main__':
    print(find_by_tag('li'))