from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Docker health checks"""
    try:
        # Test that cowsay command is available
        result = subprocess.run(['cowsay', '--version'], capture_output=True, text=True, check=True)
        return jsonify({
            'status': 'healthy',
            'service': 'cowsay',
            'version': 'cowsay available',
            'timestamp': __import__('time').time()
        })
    except subprocess.CalledProcessError:
        return jsonify({
            'status': 'unhealthy',
            'error': 'cowsay command not available'
        }), 500

@app.route('/cowsay', methods=['POST'])
def cowsay():
    data = request.get_json()
    text = data.get('text', 'Moo!')
    
    try:
        result = subprocess.run(['cowsay', text], capture_output=True, text=True, check=True)
        return jsonify({'cowsayOutput': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
