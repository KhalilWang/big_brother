from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# 配置文件路径
generated_config_path = '../deploy/prometheus.yml'
prometheus_reload_url = 'http://localhost:9090/-/reload'

def generate_prometheus_config(data_list):
    global_config = "global:\n  scrape_interval: 15s\n\nscrape_configs:\n"

    data_list.append({
        "job_name": "Prometheus",
        "url": "localhost:9090"
    })

    scrape_configs = ""
    for data in data_list:
        scrape_configs += f"  - job_name: {data['job_name']}\n    static_configs:\n      - targets:\n        - \"{data['url']}\"\n"
    scrape_configs += """
  - job_name: 'loki'
    dns_sd_configs:
      - names:
          - loki-read
          - loki-write
          - loki-backend
        type: A
        port: 3100
        
#  - job_name: 'promtail'
#    dns_sd_configs:
#      - names:
#          - promtail
#        type: A
#        port: 9080
"""
    scrape_configs += "\n"

    return f"{global_config}{scrape_configs}"

def reload_prometheus_config():
    try:
        response = requests.post(prometheus_reload_url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to reload Prometheus config: {e}")
        return False

@app.route('/generate_config', methods=['POST'])
def generate_config():
    try:
        data_list = request.json

        # 调试输出，查看接收到的数据
        print('Received JSON data:', data_list)

        if not data_list or not all('url' in data and 'job_name' in data for data in data_list):
            return jsonify({'error': 'Invalid data format'}), 400

        prometheus_config = generate_prometheus_config(data_list)

        # 将生成的 Prometheus 配置写入文件到指定目录
        with open(generated_config_path, 'w') as prom_file:
            prom_file.write(prometheus_config)

        # 重新加载 Prometheus 配置
        if reload_prometheus_config():
            return jsonify({'message': 'Prometheus config generated and reloaded successfully'}), 200
        else:
            return jsonify({'error': 'Failed to reload Prometheus config'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11451)