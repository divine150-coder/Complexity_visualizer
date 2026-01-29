from flask import Flask, request, jsonify
import time
import matplotlib.pyplot as plt
import io
import base64
import random

app = Flask(__name__)

# Example algorithms
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def linear_search(arr, target):
    for i in arr:
        if i == target:
            return True
    return False

def binary_search(arr, target):
    arr.sort()
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left + right)//2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False

def nested_exponential(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += i*j
    return total

@app.route("/analyze")
def analyze():
    algo = request.args.get("algo", "bubble").lower()
    n = int(request.args.get("n", 1000))
    steps = int(request.args.get("steps", 10))
    
    times = []
    step_values = list(range(1, n+1, max(1, n//steps)))

    for step in step_values:
        arr = [random.randint(1, 1000) for _ in range(step)]
        start = time.time()
        if algo == "bubble":
            bubble_sort(arr)
        elif algo == "linear":
            linear_search(arr, random.randint(1,1000))
        elif algo == "binary":
            binary_search(arr, random.randint(1,1000))
        elif algo == "nested":
            nested_exponential(step)
        else:
            return jsonify({"error": "Unknown algorithm"}), 400
        end = time.time()
        times.append(end - start)
    
    # Create graph
    plt.figure()
    plt.plot(step_values, times, marker='o')
    plt.title(f"{algo.capitalize()} Performance")
    plt.xlabel("Number of Elements (n)")
    plt.ylabel("Time (s)")
    plt.grid(True)
    
    # Convert plot to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    total_time = sum(times)
    
    response = {
        "algorithm": algo,
        "n": n,
        "steps": steps,
        "step_values": step_values,
        "times": times,
        "total_time": total_time,
        "graph_base64": img_base64
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=3000, debug=True)

