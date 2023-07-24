# Установіть необхідні бібліотеки перед виконанням скрипту:
# pip install pymongo[srv]
# pip install mongoengine

from mongoengine import Document, connect, StringField, ReferenceField, ListField

# Підключення до хмарної бази даних MongoDB (Atlas)
connect("mongodb+srv://akashyren77:<password>@whw8.ludjncu.mongodb.net/?retryWrites=true&w=majority")

# Модель автора
class Author(Document):
    name = StringField(required=True, unique=True)

# Модель цитати
class Quote(Document):
    text = StringField(required=True)
    author = ReferenceField(Author)
    tags = ListField(StringField())

# Код для завантаження json файлів у хмарну базу даних

def load_data_to_database():
    # Завантаження даних для колекції authors
    with open("authors.json", "r", encoding="utf-8") as f:
        authors_data = f.read()
        for author_data in authors_data:
            author = Author(name=author_data["name"])
            author.save()

    # Завантаження даних для колекції quotes
    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes_data = f.read()
        for quote_data in quotes_data:
            author_name = quote_data.pop("author")
            author = Author.objects.get(name=author_name)
            quote = Quote(author=author, **quote_data)
            quote.save()

# Реалізуйте функцію для пошуку цитат за тегом, за ім'ям автора або набором тегів

def search_quotes():
    while True:
        command = input("Команда: ")
        parts = command.split(":")
        if parts[0] == "exit":
            break
        elif parts[0] == "name":
            author_name = parts[1].strip()
            author = Author.objects.get(name=author_name)
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.text)
        elif parts[0] == "tag":
            tag = parts[1].strip()
            quotes = Quote.objects(tags=tag)
            for quote in quotes:
                print(quote.text)
        elif parts[0] == "tags":
            tags = [tag.strip() for tag in parts[1].split(",")]
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(quote.text)
        else:
            print("Невідома команда. Спробуйте ще раз.")

if __name__ == "__main__":
    # Завантаження даних у хмарну базу даних
    load_data_to_database()

    # Виклик функції для пошуку цитат
    search_quotes()
