from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

application = FastAPI()

application.mount('/static', StaticFiles(directory='static'))

templates = Jinja2Templates(directory='templates')


class Book:
    __slots__ = ['id', 'name', 'author', 'year', 'count']

    def __init__(self, id:int, name: str, author: str, year: str, count: str):
        self.id = id
        self.name = name
        self.author = author
        self.year = year
        self.count = count


books = [
    Book(1, 'Konan', 'unknown', 1898, 1),
    Book(2, 'Sherlock', 'Konan', 1243, 2),
    Book(3, 'Sherlock_2', 'Konan', 1243, 1)
]


@application.get('/books', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'books': books})


@application.get('/books/{book_id}', response_class=HTMLResponse)
async def book(book_id: int, request: Request):
    target_book = None
    for book in books:
        if book.id == book_id:
            target_book = book
            break
    if not target_book:
        raise HTTPException(status_code=404, detail='Book is not found')
    return templates.TemplateResponse('index.html', {'request': request,'book': target_book})
