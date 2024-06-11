from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/run-tests', methods=['POST'])
def run_tests():
    try:
        result = subprocess.run(['pytest', '--junitxml=results.xml'], capture_output=True, text=True)
        with open('results.xml', 'r') as file:
            test_results = file.read()
        return jsonify({'output': result.stdout, 'results': test_results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
