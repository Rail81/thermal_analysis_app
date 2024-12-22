# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import griddata

class ThermalPointAnalytics:
    def __init__(self, thermal_points):
        """
        Инициализация аналитики по точкам измерения
        
        :param thermal_points: Список точек измерения
        """
        self.points = thermal_points
        self.df = self._prepare_dataframe()

    def _prepare_dataframe(self):
        """
        Преобразование точек в DataFrame
        """
        return pd.DataFrame([
            {
                'x': point.x_coordinate, 
                'y': point.y_coordinate, 
                'temperature': point.temperature
            } for point in self.points
        ])

    def temperature_distribution_analysis(self):
        """
        Анализ распределения температуры
        """
        return {
            'mean_temperature': self.df['temperature'].mean(),
            'median_temperature': self.df['temperature'].median(),
            'temperature_std': self.df['temperature'].std(),
            'min_temperature': self.df['temperature'].min(),
            'max_temperature': self.df['temperature'].max()
        }

    def generate_heatmap(self, output_path):
        """
        Генерация тепловой карты распределения температур
        
        :param output_path: Путь для сохранения изображения
        """
        # Интерполяция данных для гладкой визуализации
        x = self.df['x']
        y = self.df['y']
        z = self.df['temperature']

        xi = np.linspace(x.min(), x.max(), 100)
        yi = np.linspace(y.min(), y.max(), 100)
        xi, yi = np.meshgrid(xi, yi)
        
        # Интерполяция температур
        zi = griddata((x, y), z, (xi, yi), method='cubic')

        plt.figure(figsize=(10, 8))
        plt.title('Распределение температур')
        contour = plt.contourf(xi, yi, zi, levels=20, cmap='hot')
        plt.colorbar(contour, label='Температура (°C)')
        plt.scatter(x, y, c=z, cmap='hot', edgecolors='black')
        plt.xlabel('X координата')
        plt.ylabel('Y координата')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def temperature_gradient_analysis(self):
        """
        Анализ градиента температуры
        """
        # Вычисление локальных градиентов температуры
        df_sorted = self.df.sort_values(['x', 'y'])
        df_sorted['temp_gradient_x'] = df_sorted['temperature'].diff()
        df_sorted['temp_gradient_y'] = df_sorted['temperature'].diff(axis=0)

        return {
            'max_x_gradient': df_sorted['temp_gradient_x'].abs().max(),
            'max_y_gradient': df_sorted['temp_gradient_y'].abs().max(),
            'avg_x_gradient': df_sorted['temp_gradient_x'].abs().mean(),
            'avg_y_gradient': df_sorted['temp_gradient_y'].abs().mean()
        }

    def export_to_csv(self, output_path):
        """
        Экспорт данных в CSV
        
        :param output_path: Путь для сохранения CSV
        """
        self.df.to_csv(output_path, index=False, encoding='utf-8')

    def risk_assessment(self):
        """
        Оценка рисков на основе температурных данных
        """
        stats = self.temperature_distribution_analysis()
        gradient_stats = self.temperature_gradient_analysis()

        risk_score = 0
        risk_factors = []

        # Критерии оценки риска
        if stats['max_temperature'] > 80:  # Высокая температура
            risk_score += 3
            risk_factors.append("Экстремально высокая температура")
        
        if gradient_stats['max_x_gradient'] > 10:  # Резкие перепады
            risk_score += 2
            risk_factors.append("Значительные температурные градиенты")
        
        risk_level = (
            "Критический" if risk_score > 4 else
            "Высокий" if risk_score > 2 else
            "Средний" if risk_score > 1 else
            "Низкий"
        )

        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            **stats,
            **gradient_stats
        }
