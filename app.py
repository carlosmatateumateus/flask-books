from flaskr import app
from flask import g, request, abort

@app.route('/', methods=['GET'])
def index():       
    books = g.db.cursor().execute('SELECT * FROM books;')
    return [dict(
                id=books[0], title=books[1],
                description=books[2], price=books[3]
            ) 
    for books in books.fetchall()], 200


@app.route('/create', methods=['POST'])
def create():
    try:
        g.db.cursor().execute(f'''
        INSERT INTO books(title, price, description) 
        VALUES("{request.json['title']}", "{request.json['price']}", "{request.json['description']}"
        );
        ''')
        
        return 'product has been created.', 201
    except:
        return abort(400)


@app.route('/read/<int:id>', methods=['GET'])
def read(id):
    try:
        return [dict(
                    id=element[0], title=element[1],
                    description=element[2], price=element[3]
                ) 
        for element in g.db.cursor().execute(f'SELECT * FROM books WHERE id == {id};').fetchall()
        ][0], 200
    except:
        return abort(404)       


@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    if not len(list(g.db.cursor().execute(f'SELECT * FROM books WHERE id=={id};'))) == 1:
        return abort(404)
    else: 
        try:
            g.db.cursor().execute(f'''
            UPDATE books SET title="{request.json['title']}",
            description="{request.json['description']}",
            price="{request.json['price']}" WHERE id=={id};
            ''')

            return 'product has been updated', 202
        except:
            return abort(400)
    

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        g.db.cursor().execute(f'DELETE FROM books WHERE id={id}')

        return 'product has been deleted', 200
    except:
        return abort(400)
    
    
if __name__=='__main__':
    app.run()