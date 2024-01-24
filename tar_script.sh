#!/bin/bash

# 默认操作是显示帮助信息
operation="usage"

# 解析命令行参数
while getopts ":cxh" opt; do
  case ${opt} in
    c )
      operation="compress"
      ;;
    x )
      operation="decompress"
      ;;
    h )
      operation="usage"
      ;;
    \? )
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# 根据操作执行相应的命令
case ${operation} in
  compress )
    tar -czvf big_brother_deploy.tar.gz ./deploy/*
    tar -czvf little_brother.tar.gz ./little_brother/*
    ;;
  decompress )
    tar -xzvf big_brother_deploy.tar.gz -C ./
    tar -xzvf little_brother.tar.gz -C ./
    ;;
  usage )
    echo "Usage: $0 [-c | -x | -h]"
    echo "  -c: Compress files"
    echo "  -x: Decompress files"
    echo "  -h: Display this help message"
    ;;
esac