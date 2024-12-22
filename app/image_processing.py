import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class ImageManager:
    def __init__(self, base_dir='app/static/uploads'):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        
        # Поддиректории
        self.subdirs = {
            'thermogram': os.path.join(base_dir, 'thermograms'),
            'equipment': os.path.join(base_dir, 'equipment'),
            'reports': os.path.join(base_dir, 'reports')
        }
        
        for subdir in self.subdirs.values():
            os.makedirs(subdir, exist_ok=True)

    def save_thermogram(self, image, equipment_name):
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{equipment_name}_{timestamp}_thermogram.png"
        filepath = os.path.join(self.subdirs['thermogram'], filename)
        
        plt.figure(figsize=(10, 8))
        plt.imshow(image, cmap='hot')
        plt.colorbar(label='Температура, °C')
        plt.title(f'Термограмма {equipment_name}')
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        
        return filepath

    def generate_thermal_analysis(self, thermogram):
        """
        Базовый анализ термограммы
        """
        return {
            'max_temperature': np.max(thermogram),
            'min_temperature': np.min(thermogram),
            'avg_temperature': np.mean(thermogram)
        }

class ThermalOverloadCalculator:
    def __init__(self):
        # Справочник порогов для разных типов оборудования
        self.equipment_thresholds = {
            'transformer': {
                'normal_temp': 65,
                'warning_temp': 75,
                'critical_temp': 85
            }
        }

    def calculate_thermal_overload(self, current_temp, equipment_type='transformer', load_factor=1.0):
        thresholds = self.equipment_thresholds.get(equipment_type, 
                                                   self.equipment_thresholds['transformer'])
        
        # Корректировка порогов с учетом нагрузки
        adjusted_normal = thresholds['normal_temp'] * load_factor
        adjusted_warning = thresholds['warning_temp'] * load_factor
        adjusted_critical = thresholds['critical_temp'] * load_factor
        
        # Определение статуса перегрева
        if current_temp > adjusted_critical:
            return {
                'status': 'critical',
                'risk_level': 3
            }
        elif current_temp > adjusted_warning:
            return {
                'status': 'warning',
                'risk_level': 2
            }
        elif current_temp > adjusted_normal:
            return {
                'status': 'elevated',
                'risk_level': 1
            }
        
        return {
            'status': 'normal',
            'risk_level': 0
        }
