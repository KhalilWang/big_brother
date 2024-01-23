from flask import Flask, request, jsonify

app = Flask(__name__)

# 配置文件路径
template_file_path = 'prometheus_template.yml'

def generate_prometheus_config(data_list):
    global_config = "global:\n  scrape_interval: 15s\n\nscrape_configs:\n"
    
    scrape_configs = ""
    for data in data_list:
        scrape_configs += f"  - job_name: {data['job_name']}\n    static_configs:\n      - targets:\n        - {data['url']}\n"

    return f"{global_config}{scrape_configs}"

@app.route('/generate_config', methods=['POST'])
def generate_config():
    try:
        data_list = request.json

        # 调试输出，查看接收到的数据
        print('Received JSON data:', data_list)

        if not data_list or not all('url' in data and 'job_name' in data for data in data_list):
            return jsonify({'error': 'Invalid data format'}), 400

        prometheus_config = generate_prometheus_config(data_list)

        # 将生成的 Prometheus 配置写入文件（或进行其他处理）
        with open('prometheus_generated_config.yml', 'w') as prom_file:
            prom_file.write(prometheus_config)

        return jsonify({'message': 'Prometheus config generated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11451)
