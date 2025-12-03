import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AdvancedCodeAnalyzer:
    def __init__(self, directory):
        self.directory = directory
        self.vulnerabilities = defaultdict(list)
        self.sensitive_functions = ['eval', 'exec', 'os.system', 'subprocess.call', 'open']
        
        self.patterns = {
            'sql_injection': r'(SELECT|INSERT|UPDATE|DELETE)\s+',
            'xss': r'<script>',
            'command_injection': r'\$\(.*\)'
        }
        
        self.df = pd.DataFrame(columns=['file', 'line', 'vulnerability', 'description'])

    def scan_directory(self):
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.py'):
                    self.analyze_file(os.path.join(root, file))

    def analyze_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()
                self.check_sensitive_functions(content, file_path)
                self.check_patterns(content, file_path)
                self.analyze_code_complexity(content, file_path)
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")

    def check_sensitive_functions(self, content, file_path):
        for line_num, line in enumerate(content, 1):
            for func in self.sensitive_functions:
                if func in line:
                    self.vulnerabilities['sensitive_functions'].append(
                        f"{file_path}:{line_num}: Обнаружена опасная функция {func}"
                    )
                    self.df = self.df.append({
                        'file': file_path,
                        'line': line_num,
                        'vulnerability': 'sensitive_function',
                        'description': f'Обнаружена опасная функция {func}'
                    }, ignore_index=True)

    def check_patterns(self, content, file_path):
        for line_num, line in enumerate(content, 1):
            for pattern_name, pattern in self.patterns.items():
                if re.search(pattern, line):
                    self.vulnerabilities[pattern_name].append(
                        f"{file_path}:{line_num}: Обнаружен паттерн {pattern_name}"
                    )
                    self.df = self.df.append({
                        'file': file_path,
                        'line': line_num,
                        'vulnerability': pattern_name,
                        'description': f'Обнаружен паттерн {pattern_name}'
                    }, ignore_index=True)

    def analyze_code_complexity(self, content, file_path):
        # Анализ сложности кода
        code_text = ' '.join(content)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([code_text])
        
        # Расчет метрик сложности
        complexity_score = np.mean(tfidf_matrix.toarray())
        unique_words = len(vectorizer.get_feature_names_out())
        
        if complexity_score > 0.5 or unique_words > 100:
            self.df = self.df.append({
                'file': file_path,
                'line': 'Весь файл',
                'vulnerability': 'high_complexity',
                'description': f'Высокая сложность кода (score: {complexity_score:.2f}, уникальных слов: {unique_words})'
            }, ignore_index=True)

    def generate_report(self):
        report = "Отчет по анализу безопасности:\n"
        for vulnerability_type, findings in self.vulnerabilities.items():
            report += f"\n{vulnerability_type.upper()}:\n"