# Big Brother

## what is big_brother

- deploy 使用 docker-compose 部署 loki 和 prom 服务器，并添加了默认配置
- little_brother 接收 http 请求，然后修改 prom 服务器配置，然后发送 reload 请求到 prom 服务器

## usage

- tar_script.sh 打包文件，需要手动发送到 GCP 节点进行部署
- deploy 目录下直接使用 `docker-compose up -d` 即可
- little_brother 使用方法：
    0. 拥有 python3 环境
    1. 进入 little_brother 下创建 venv 环境 `python3 -m venv.`
    2. 安装依赖 `sh python_install.sh`
    3. 运行 little_brother `sh start.sh`
    4. 观察 nohup.out 文件输出后，去对应的 4000 M1x后台服务器使用节点嗅探功能