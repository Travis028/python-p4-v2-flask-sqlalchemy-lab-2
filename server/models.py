from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # Add relationship to Review
    reviews = db.relationship('Review', back_populates='customer')
    
    # Add association proxy WITH creator function
    items = association_proxy('reviews', 'item',
                             creator=lambda item_obj: Review(item=item_obj, comment="New item added"))
    
    # Serialization rules
    serialize_rules = ('-reviews.customer',)
    
    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    # Add relationship to Review
    reviews = db.relationship('Review', back_populates='item')
    
    # Serialization rules
    serialize_rules = ('-reviews.item',)
    
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')
    
    # Serialization rules
    serialize_rules = ('-customer.reviews', '-item.reviews',)
    
    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'