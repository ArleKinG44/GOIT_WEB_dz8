from mongoengine.errors import NotUniqueError
from models import Author, Quote
import json

def load_data_to_cloud_db(cloud_db_url, collection_name, file_path):
    connect(db=collection_name, host=cloud_db_url)
    # connect(db=test, host=mongodb://localhost:27017)
    with open(file_path, encoding='utf-8') as fd:
        data = json.load(fd)
        if collection_name == 'autors':
            for el in data:
                try:
                    author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                    born_location=el.get('born_location'), description=el.get('description'))
                    author.save()
                except NotUniqueError:
                    print(f"Автор вже існує {el.get('fullname')}")
        elif collection_name == 'quotes':
            for el in data:
                author = Author.objects(fullname=el.get('author')).first()
                quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
                quote.save()

def search_quotes(query):
    if query.startswith('name:'):
        author_name = query.split(':')[1].strip()
        authors = Author.objects(fullname__icontains=author_name)
        result = {}
        for author in authors:
            quotes = Quote.objects(author=author)
            result[author.fullname] = [quote.quote for quote in quotes]
        return result
    elif query.startswith('tag:'):
        tag = query.split(':')[1].strip()
        quotes = Quote.objects(tags__icontains=tag)
        return [quote.quote for quote in quotes]
    elif query.startswith('tags:'):
        tags = query.split(':')[1].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        return [quote.quote for quote in quotes]
    elif query == 'exit':
        return "Exiting script..."
    else:
        return "Invalid query format."

if __name__ == '__main__':
    load_data_to_cloud_db("mongodb://localhost:27017", "autors", "C:/VS_projekts/GOIT_WEB_dz8/autors.json")
    load_data_to_cloud_db("mongodb://localhost:27017", "quotes", "C:/VS_projekts/GOIT_WEB_dz8/qoutes.json")

    while True:
        user_input = input("Enter command (name:<author_name>, tag:<tag>, tags:<tag1,tag2>, or exit): ")
        result = search_quotes(user_input)
        if isinstance(result, dict):
            for author, quotes in result.items():
                print(f"Quotes by {author}:")
                for quote in quotes:
                    print(quote)
        elif isinstance(result, list):
            print("Quotes:")
            for quote in result:
                print(quote)
        else:
            print(result)
        if result == "Exiting script...":
            break
