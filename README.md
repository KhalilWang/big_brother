# Big Brother

## what is big_brother

- deploy 使用 docker-compose 部署 loki 和 prom 服务器，并添加了默认配置
- little_brother 接收 http 请求，然后修改 prom 服务器配置，然后发送 reload 请求到 prom 服务器

## usage

- tar_script.sh 打包文件，需要手动发送到 GCP 节点进行部署
- deploy 目录下直接使用 `docker-compose up -d` 即可
- little_brother 下使用 `source venv/bin/activate` 然后使用 `sh start.sh` 脚本拉起 http svr