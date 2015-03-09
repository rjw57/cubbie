"""
Database models for cubbie.

"""
from flask.ext.sqlalchemy import SQLAlchemy

# This needs to be created outside of create_...() in order that Models can be
# defined
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    displayname = db.Column(db.Text, nullable=False)

db.Index('idx_user_displayname', User.displayname)

class Production(db.Model):
    __tablename__ = 'productions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    productions = db.relationship('Performance', backref='production')

db.Index('idx_production_name', Production.name)

class Performance(db.Model):
    __tablename__ = 'performances'

    id = db.Column(db.Integer, primary_key=True)
    starts_at = db.Column(db.DateTime(timezone=True), nullable=False)
    duration = db.Column(db.Interval(native=True), nullable=False)
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'),
            nullable=False)
    is_cancelled = db.Column(db.Boolean, nullable=False, default=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

db.Index('idx_performance_production', Performance.production_id)
db.Index('idx_performance_starts_at', Performance.starts_at)
db.Index('idx_performance_is_cancelled', Performance.is_cancelled)
db.Index('idx_performance_is_deleted', Performance.is_deleted)

class SalesDatum(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    measured_at = db.Column(db.DateTime(timezone=True), nullable=False)
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'),
            nullable=False)
    is_valid = db.Column(db.Boolean, nullable=False, default=False)
    sold = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)

db.Index('idx_sales_production', SalesDatum.production_id)
db.Index('idx_sales_measured_at', SalesDatum.measured_at)
db.Index('idx_sales_is_valid', SalesDatum.is_valid)
