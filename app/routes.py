# -*- coding: utf-8 -*-
import os
import base64
import json
import csv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from app import db
from app.models import Equipment, ThermalAnalysis, ThermalPoint
from app.image_processing import ImageManager, ThermalOverloadCalculator
from app.thermal_point_analytics import ThermalPointAnalytics
import numpy as np
from PIL import Image

# Создаем Flask-приложение
app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')

@app.route('/')
def index():
    """
    Главная страница с навигацией между разделами
    """
    return render_template('index.html')

@app.route('/thermogram_analysis')
def thermogram_analysis():
    """
    Страница интерактивного анализа термограмм
    """
    return render_template('index.html')

@app.route('/save_thermogram_analysis', methods=['POST'])
def save_thermogram_analysis():
    """
    Сохранение результатов анализа термограммы
    """
    data = request.json
    points = data.get('points', [])
    image_data = data.get('image', '')

    # Базовая обработка и сохранение
    thermal_analysis = ThermalAnalysis(
        max_temperature=max([float(p['temperature']) for p in points], default=0),
        min_temperature=min([float(p['temperature']) for p in points], default=0),
        avg_temperature=sum(float(p['temperature']) for p in points) / len(points) if points else 0,
        risk_level='средний'  # Временно фиксированное значение
    )
    db.session.add(thermal_analysis)
    db.session.commit()

    # Сохраняем точки измерения
    for point in points:
        thermal_point = ThermalPoint(
            analysis_id=thermal_analysis.id,
            x_coordinate=point['x'],
            y_coordinate=point['y'],
            temperature=float(point['temperature']),
            description=point.get('description', '')
        )
        db.session.add(thermal_point)
    
    db.session.commit()

    return jsonify({
        'analysis_id': thermal_analysis.id,
        'risk_assessment': {
            'risk_level': 'средний',
            'risk_score': 3
        }
    })

@app.route('/advanced_analysis/<int:analysis_id>')
def advanced_analysis(analysis_id):
    """
    Расширенная аналитика для конкретного анализа
    """
    analysis = ThermalAnalysis.query.get_or_404(analysis_id)
    points = ThermalPoint.query.filter_by(analysis_id=analysis_id).all()
    
    return render_template('index.html', 
                           analysis=analysis, 
                           points=points)

@app.route('/analysis_export/<int:analysis_id>')
def analysis_export(analysis_id):
    """
    Экспорт результатов анализа
    """
    analysis = ThermalAnalysis.query.get_or_404(analysis_id)
    points = ThermalPoint.query.filter_by(analysis_id=analysis_id).all()
    
    # Временно возвращаем JSON
    export_data = {
        'analysis_id': analysis.id,
        'max_temperature': analysis.max_temperature,
        'min_temperature': analysis.min_temperature,
        'avg_temperature': analysis.avg_temperature,
        'points': [
            {
                'x': point.x_coordinate, 
                'y': point.y_coordinate, 
                'temperature': point.temperature,
                'description': point.description
            } for point in points
        ]
    }
    
    return jsonify(export_data)

if __name__ == '__main__':
    app.run(debug=True)
