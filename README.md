# 打开基于docker的Milvus服务器（前提是已经下载了Milvus镜像）

- 前往存放了docker-compose.yml的文件夹（docker-compose.yml是从官网下载的milvus-standalone-docker-compose.yml，并重命名为docker-compose.yml）
- 运行命令 `docker-compose up -d` ,如果您希望在后台运行容器并隐藏日志等输出，可以使用 -d（--detach）选项
- 然后检查containers是否正在运行:`docker-compose ps`
- 当Milvus standalone 开启, 会有3个 docker containers 运行, 包括 Milvus standalone 服务和它的两个依赖:

| Name              | Command                        | State        | Ports                                        |
| ----------------- | ------------------------------ | ------------ | -------------------------------------------- |
| milvus-etcd       | etcd -listen-peer-urls=htt ... | Up (healthy) | 2379/tcp, 2380/tcp                           |
| milvus-minio      | /usr/bin/docker-entrypoint ... | Up (healthy) | 9000/tcp                                     |
| milvus-standalone | /tini -- milvus run standalone | Up           | 0.0.0.0:19530->19530/tcp,:::19530->19530/tcp |

- 要停止Milvus standalone, 运行: `docker-compose down`
- 停止Milvus standalone后清除数据，运行 `rm -rf  volumes`

# 在windows环境中使用的差异

## 关于windows激活虚拟环境的方式

`venv\Scripts\activate.ps1`

注意：

- 默认情况下在计算机上启动 Windows PowerShell 时，执行策略很可能是 Restricted。Restricted 执行策略不允许任何脚本运行。AllSigned 和 RemoteSigned 执行策略可防止 Windows PowerShell 运行没有数字签名的脚本。
- 想了解 计算机上的现用执行策略，打开 PowerShell 然后输入 get-executionpolicy。默认情况下返回的是 Restricted 。
- 以管理员身份打开PowerShell 输入 set-executionpolicy remotesigned ，就可以正常在 PowerShell 中运行 ps1 文件了

## 关于虚拟环境内使用pip安装依赖包

在Windows中，使用虚拟环境安装依赖包时，不能直接使用pip命令。你需要先切换到虚拟环境的Scripts文件夹下，然后使用 `venv\Scripts\python.exe -m pip install`命令安装依赖包。这样安装的包只会在当前的虚拟环境中起作用，避免了污染系统环境

# 关于模型

## 从hugging face 寻找模型

- 最好使用显卡的运行环境，因为模型的调用需要显卡的算力
- 直接使用代码调用的话，会先下载模型到缓存，其实这种方式也可以直接下载模型到本地然后通过文件路径调用
- 应该也有直接远程调用模型的方式，之后研究一下

## 关于显存

运行本地模型时报错：

```bash
torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 128.00 MiB (GPU 0; 6.00 GiB total capacity; 5.25 GiB already allocated; 0 bytes free; 5.25 GiB reserved in total by PyTorch) If reserved memory is >> allocated memory try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF
```

显卡还是太小了啊。



# 程序逻辑

## 总体逻辑
