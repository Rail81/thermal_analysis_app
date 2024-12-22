# -*- coding: utf-8 -*-
from app import db
from datetime import datetime

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispatcher_name = db.Column(db.String(100), nullable=False)
    equipment_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    thermal_analyses = db.relationship('ThermalAnalysis', backref='equipment', lazy=True)

class ThermalAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    thermogram_path = db.Column(db.String(255))
    max_temperature = db.Column(db.Float)
    min_temperature = db.Column(db.Float)
    avg_temperature = db.Column(db.Float)
    overload_status = db.Column(db.String(50))
    risk_level = db.Column(db.String(20))
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    thermal_points = db.relationship('ThermalPoint', backref='analysis', lazy=True)

class ThermalPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('thermal_analysis.id'), nullable=False)
    x_coordinate = db.Column(db.Float, nullable=False)
    y_coordinate = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    measurement_time = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x_coordinate,
            'y': self.y_coordinate,
            'temperature': self.temperature,
            'description': self.description
        }
