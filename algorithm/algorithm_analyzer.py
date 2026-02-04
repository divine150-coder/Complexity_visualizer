#!/usr/bin/env python3
"""Algorithm Analysis Flask API with Database Storage and Graph Generation"""

import time
import random
import base64
import io
import json
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

app = Flask(__name__)

# Database setup
DATABASE_URL = "mysql+pymysql://root:spatni@localhost:3306/hbnb_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class AlgorithmAnalysis(Base):
    __tablename__ = 'algorithm_analysis'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    algo = Column(String(100), nullable=False)
    items = Column(Integer, nullable=False)
    steps = Column(Integer, nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    total_time_ms = Column(Float, nullable=False)
    time_complexity = Column(String(50), nullable=False)
    path_to_graph = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)

def bubble_sort(arr):
    """Bubble sort implementation"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def linear_search(arr, target):
    """Linear search implementation"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr, target):
    """Binary search implementation"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def nested_exponential(n):
    """Nested/exponential algorithm simulation"""
    count = 0
    for i in range(n):
        for j in range(n):
            for k in range(min(100, n)):  # Cap to prevent excessive computation
                count += 1
    return count

def get_time_complexity(algo):
    """Return time complexity for each algorithm"""
    complexities = {
        'bubble': 'O(n²)',
        'linear': 'O(n)',
        'binary': 'O(log n)',
        'nested': 'O(n³)',
        'exponential': 'O(n³)'
    }
    return complexities.get(algo, 'O(n)')

def generate_performance_graph(algo, n_values, times):
    """Generate performance graph and return base64 encoded image"""
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times, 'b-o', linewidth=2, markersize=6)
    plt.title(f'{algo.title()} Algorithm Performance Analysis', fontsize=14, fontweight='bold')
    plt.xlabel('Input Size (n)', fontsize=12)
    plt.ylabel('Execution Time (ms)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return image_base64

def run_algorithm_analysis(algo, n, steps):
    """Run algorithm analysis and return performance data"""
    step_size = max(1, n // steps)
    n_values = list(range(step_size, n + 1, step_size))
    times = []
    
    for current_n in n_values:
        # Generate test data
        if algo in ['bubble']:
            test_data = [random.randint(1, 1000) for _ in range(current_n)]
        elif algo in ['linear', 'binary']:
            test_data = list(range(current_n))
            target = random.choice(test_data)
        else:  # nested/exponential
            test_data = current_n
        
        # Measure execution time
        start_time = time.perf_counter()
        
        if algo == 'bubble':
            bubble_sort(test_data.copy())
        elif algo == 'linear':
            linear_search(test_data, target)
        elif algo == 'binary':
            binary_search(test_data, target)
        elif algo in ['nested', 'exponential']:
            nested_exponential(min(current_n, 50))  # Cap for performance
        
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000
        times.append(execution_time_ms)
    
    return n_values, times

@app.route('/analyze', methods=['GET'])
def analyze_algorithm():
    """Analyze algorithm performance and return results with graph"""
    try:
        # Get query parameters
        algo = request.args.get('algo', '').lower()
        n = int(request.args.get('n', 100))
        steps = int(request.args.get('steps', 10))
        
        # Validate algorithm
        valid_algos = ['bubble', 'linear', 'binary', 'nested', 'exponential']
        if algo not in valid_algos:
            return jsonify({
                'error': 'Invalid algorithm',
                'valid_algorithms': valid_algos
            }), 400
        
        # Record overall start time
        overall_start = time.perf_counter()
        
        # Run analysis
        n_values, times = run_algorithm_analysis(algo, n, steps)
        
        # Generate graph
        graph_base64 = generate_performance_graph(algo, n_values, times)
        
        # Record overall end time
        overall_end = time.perf_counter()
        total_analysis_time = (overall_end - overall_start) * 1000
        
        # Prepare response
        response = {
            'algo': f'{algo} sort' if algo == 'bubble' else f'{algo} search' if algo in ['linear', 'binary'] else f'{algo} algorithm',
            'items': n,
            'steps': steps,
            'start_time': int(overall_start * 1000000),  # microseconds
            'end_time': int(overall_end * 1000000),      # microseconds
            'total_time_ms': round(total_analysis_time, 3),
            'time_complexity': get_time_complexity(algo),
            'path_to_graph': f'data:image/png;base64,{graph_base64}',
            'performance_data': {
                'n_values': n_values,
                'execution_times_ms': [round(t, 3) for t in times]
            }
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/save_analysis', methods=['POST'])
def save_analysis():
    """Save algorithm analysis results to database"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['algo', 'items', 'steps', 'start_time', 'end_time', 'total_time_ms', 'time_complexity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create database session
        session = Session()
        
        # Create new analysis record
        analysis = AlgorithmAnalysis(
            algo=data['algo'],
            items=data['items'],
            steps=data['steps'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            total_time_ms=data['total_time_ms'],
            time_complexity=data['time_complexity'],
            path_to_graph=data.get('path_to_graph', '')
        )
        
        # Save to database
        session.add(analysis)
        session.commit()
        
        # Get the ID of the saved record
        analysis_id = analysis.id
        session.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Analysis saved successfully',
            'analysis_id': analysis_id,
            'created_at': analysis.created_at.isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to save analysis: {str(e)}'
        }), 500

@app.route('/retrieve_analysis', methods=['GET'])
def retrieve_analysis():
    """Retrieve algorithm analysis by ID"""
    try:
        analysis_id = request.args.get('id')
        
        if not analysis_id:
            return jsonify({'error': 'Missing analysis ID parameter'}), 400
        
        # Create database session
        session = Session()
        
        # Query analysis by ID
        analysis = session.query(AlgorithmAnalysis).filter_by(id=analysis_id).first()
        
        if not analysis:
            session.close()
            return jsonify({'error': f'Analysis with ID {analysis_id} not found'}), 404
        
        # Prepare response
        response = {
            'id': analysis.id,
            'algo': analysis.algo,
            'items': analysis.items,
            'steps': analysis.steps,
            'start_time': int(analysis.start_time),
            'end_time': int(analysis.end_time),
            'total_time_ms': analysis.total_time_ms,
            'time_complexity': analysis.time_complexity,
            'path_to_graph': analysis.path_to_graph,
            'created_at': analysis.created_at.isoformat()
        }
        
        session.close()
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve analysis: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Algorithm Analyzer API',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    print("=== Algorithm Analysis API ===")
    print("Server starting on: http://localhost:3000")
    print("\nAvailable endpoints:")
    print("  GET  /analyze?algo=bubble&n=1000&steps=10")
    print("  POST /save_analysis")
    print("  GET  /retrieve_analysis?id=1")
    print("  GET  /health")
    print("\nSupported algorithms: bubble, linear, binary, nested, exponential")
    print("\nPress Ctrl+C to stop server...")
    
    app.run(host='0.0.0.0', port=3000, debug=True)
