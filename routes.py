from flask import Blueprint, request, jsonify
from app.models import db, Book
from app.models import Member
from app.models import Transaction

# Borrow a book
@api.route('/transactions/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    new_transaction = Transaction(
        book_id=data['book_id'],
        member_id=data['member_id']
    )
    book = Book.query.get_or_404(data['book_id'])
    if not book.availability:
        return jsonify({"error": "Book is not available"}), 400
    
    book.availability = False
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Book borrowed successfully"}), 201

# Return a book
    @api.route('/transactions/return/<int:id>', methods=['POST'])
    def return_book(id):
        transaction = Transaction.query.get_or_404(id)
    if transaction.return_date:
        return jsonify({"error": "Book already returned"}), 400
    
    transaction.return_date = datetime.utcnow()
    book = Book.query.get_or_404(transaction.book_id)
    book.availability = True
    db.session.commit()
    return jsonify({"message": "Book returned successfully"}), 200

# View transaction history of a member
    @api.route('/transactions/member/<int:member_id>', methods=['GET'])
    def view_transactions(member_id):
        transactions = Transaction.query.filter_by(member_id=member_id).all()
    result = []
    for transaction in transactions:
        result.append({
            'id': transaction.id,
            'book_id': transaction.book_id,
            'borrow_date': transaction.borrow_date,
            'return_date': transaction.return_date
        })
    return jsonify(result), 200

# Add a new member
    @api.route('/members', methods=['POST'])
    def add_member():
        data = request.get_json()
    new_member = Member(
        name=data['name'],
        email=data['email']
    )
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "Member added successfully"}), 201

# Retrieve member details
    @api.route('/members/<int:id>', methods=['GET'])
    def get_member(id):
        member = Member.query.get_or_404(id)
    return jsonify({
        'id': member.id,
        'name': member.name,
        'email': member.email,
        'membership_date': member.membership_date
    }), 200

# Update member information
    @api.route('/members/<int:id>', methods=['PUT'])
    def update_member(id):
        member = Member.query.get_or_404(id)
    data = request.get_json()
    member.name = data['name']
    member.email = data['email']
    db.session.commit()
    return jsonify({"message": "Member updated successfully"}), 200

# Delete a member
    @api.route('/members/<int:id>', methods=['DELETE'])
    def delete_member(id):
        member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted successfully"}), 200

api = Blueprint('api', __name__)

# Create a new book
@api.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        published_date=data['published_date'],
        ISBN=data['ISBN']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created successfully"}), 201

# Retrieve details of a specific book
@api.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'published_date': book.published_date,
        'ISBN': book.ISBN,
        'availability': book.availability
    }), 200

# Update a book entry
@api.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data['title']
    book.author = data['author']
    book.published_date = data['published_date']
    book.ISBN = data['ISBN']
    book.availability = data['availability']
    db.session.commit()
    return jsonify({"message": "Book updated successfully"}), 200

# Delete a book entry
@api.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200
@api.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@api.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad request'}), 400

@api.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
@api.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not all(key in data for key in ['title', 'author', 'published_date', 'ISBN']):
        return jsonify({"error": "Missing data"}), 400
    # Proceed with book creation...
@api.route('/books', methods=['POST'])
def create_book():
    """
    Create a new book
    ---
    parameters:
    - name: title
        in: body
        type: string
        required: true
        description: The book's title
    - name: author
        in: body
        type: string
        required: true
        description: The book's author
    # Add other parameters...
    responses:
    201:
        description: Book created successfully
    400:
        description: Invalid input data
    """
    # Route code...
