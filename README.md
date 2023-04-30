# 打开基于docker的Milvus服务器（前提是已经下载了Milvus镜像）
- 前往存放了docker-compose.yml的文件夹（docker-compose.yml是从官网下载的milvus-standalone-docker-compose.yml，并重命名为docker-compose.yml）
- 运行命令 `docker-compose up -d` ,如果您希望在后台运行容器并隐藏日志等输出，可以使用 -d（--detach）选项
- 然后检查containers是否正在运行:`docker-compose ps`
- 当Milvus standalone 开启, 会有3个 docker containers 运行, 包括 Milvus standalone 服务和它的两个依赖:

|  Name   | Command  | State|Ports |
|  ----  | ----  | ---- | ---- |
| milvus-etcd  | etcd -listen-peer-urls=htt ... | Up (healthy) | 2379/tcp, 2380/tcp |
| milvus-minio | /usr/bin/docker-entrypoint ... | Up (healthy) | 9000/tcp |
| milvus-standalone | /tini -- milvus run standalone | Up | 0.0.0.0:19530->19530/tcp,:::19530->19530/tcp |
- 要停止Milvus standalone, 运行: `docker-compose down`
- 停止Milvus standalone后清除数据，运行 `rm -rf  volumes`