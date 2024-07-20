from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

try:
    from ai.smart_contract_debugger import analyze_contract
except ImportError as e:
    analyze_contract = None
    import_error = str(e)

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/analyze', methods=['POST'])
def analyze():
    if analyze_contract is None:
        return jsonify({'error': f'TensorFlow not available: {import_error}'}), 500
    
    try:
        contract_code = request.json.get('contract_code', '')
        result = analyze_contract(contract_code)
        return jsonify({'result': result})
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
