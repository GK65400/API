from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Witaj w moim API!'

@app.route('/mojastrona')
def mojastrona():
    return 'To jest moja strona!'

@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name:
        return f'Hello {name}!'
    return 'Hello!'

@app.route('/api/v1.0/predict')
def predict():
    try:
        num1 = float(request.args.get('num1', 0))
        num2 = float(request.args.get('num2', 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    suma = num1 + num2
    prediction = 1 if suma > 5.8 else 0
    return jsonify({
        "prediction": prediction,
        "features": {
            "num1": num1,
            "num2": num2
        }
    })

@app.route('/math')
def math_operation():
    try:
        num1 = float(request.args.get('num1', 0))
        num2 = float(request.args.get('num2', 0))
        operation = request.args.get('operation', 'add')
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    result = None
    if operation == 'add':
        result = num1 + num2
    elif operation == 'sub':
        result = num1 - num2
    elif operation == 'mul':
        result = num1 * num2
    elif operation == 'div':
        result = num1 / num2 if num2 != 0 else "undefined"
    else:
        return jsonify({"error": "Unknown operation"}), 400

    return jsonify({
        "operation": operation,
        "result": result,
        "inputs": {"num1": num1, "num2": num2}
    })

# Statystyki dla podanych liczb
@app.route('/stats')
def stats():
    numbers = request.args.get('numbers')
    if not numbers:
        return jsonify({"error": "No numbers provided"}), 400

    try:
        numbers = [float(num) for num in numbers.split(',')]
    except ValueError:
        return jsonify({"error": "Invalid numbers format"}), 400

    stats = {
        "min": min(numbers),
        "max": max(numbers),
        "avg": sum(numbers) / len(numbers),
        "count": len(numbers)
    }

    return jsonify(stats)

if __name__ == '__main__':
    print("Dostępne endpointy:")
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            print(f'{rule.endpoint}: {rule}')
    app.run(debug=True, port=5000)

