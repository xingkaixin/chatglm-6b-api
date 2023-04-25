import multiprocessing

proc_name = "chatglm-6b-api"
# 绑定的ip和端口
bind = "0.0.0.0:6006"

# 使用的worker数
workers = 1

# 指定使用的worker类
worker_class = "uvicorn.workers.UvicornWorker"

# 设置debug等级
loglevel = "info"
capture_output = True
errorlog = "-"  # "-" 表示日志输出到标准错误输出（stderr）

# 设置访问日志
accesslog = "-"
access_log_format = '%(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 设置后台运行及相关配置
daemon = True
pidfile = "gunicorn.pid"
pidfile_timeout = 5
