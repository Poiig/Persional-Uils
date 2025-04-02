# mihomo-party 规则文件更新工具

这个工具用于自动下载并更新 mihomo 相关规则文件，支持 Python 和批处理两种运行方式。

## 功能

- 自动下载以下规则文件：
  - geoip.dat (来自 Loyalsoldier/v2ray-rules-dat)
  - geosite.dat (来自 Loyalsoldier/v2ray-rules-dat)
  - geoip.metadb (来自 MetaCubeX/meta-rules-dat)
  - ASN.mmdb (从 GeoLite2-ASN.mmdb 重命名)
- 自动更新用户 AppData 目录下的 mihomo-party/test 和 mihomo-party/work 目录
- 自动更新 work 子目录下的文件
- 支持自定义下载文件的 URL
- 详细的日志记录
- 多种下载方式自动尝试，提高下载成功率

## 使用方法

### 批处理脚本 (.bat)

直接双击 `update_rules_data.bat` 即可运行。

### Python 脚本

确保已安装 Python 3.6+ 和以下依赖：
```
requests
```

然后运行：
```
python update_rules_data.py
```

## 配置文件

首次运行时会自动生成配置文件 `config.ini`，可以根据需要修改下载 URL：

### Python 脚本配置格式

```ini
[URLS]
geoip.dat=https://testingcf.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geoip.dat
geosite.dat=https://testingcf.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geosite.dat
geoip.metadb=https://testingcf.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geoip.metadb
ASN.mmdb=https://gh-proxy.com/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/GeoLite2-ASN.mmdb
```

### 批处理脚本配置格式

```ini
[URLS]
GEOIP_URL=https://testingcf.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geoip.dat
GEOSITE_URL=https://testingcf.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geosite.dat
GEOIPDB_URL=https://testingcf.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geoip.metadb
ASNDB_URL=https://gh-proxy.com/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/GeoLite2-ASN.mmdb
```

## 目标目录

脚本将自动将下载的文件更新到以下目录：

- `%APPDATA%\mihomo-party\test`
- `%APPDATA%\mihomo-party\work`
- `%APPDATA%\mihomo-party\work` 下的所有子目录

注意：目录路径基于环境变量 `%APPDATA%`，不可配置。

## 下载问题排查

如果遇到下载失败，请尝试以下方法：

### 1. 检查网络连接

确保您的电脑能够正常访问互联网，特别是能够访问 GitHub 相关的服务。

### 2. 检查配置文件中的 URL

检查 `config.ini` 文件中的 URL 是否正确。如果 URL 已过期或无法访问，请尝试更新为新的可用地址。

### 3. 查看日志文件

脚本会生成详细的日志文件 `update_log.txt`，请查看以了解具体错误原因。

### 4. 常见问题及解决方法

#### 问题1: PowerShell 脚本执行策略限制

如果遇到关于 PowerShell 执行策略的错误，可以尝试以管理员身份运行 PowerShell 并执行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
```

#### 问题2: SSL/TLS 证书验证失败

如果遇到SSL证书验证错误，可以尝试在Python脚本中添加：

```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

或者尝试使用HTTP代理。

#### 问题3: 防火墙或安全软件拦截

某些安全软件可能会拦截脚本的网络请求，请尝试暂时关闭防火墙或安全软件，或将脚本添加到白名单。

#### 问题4: 无法正常解析域名

尝试修改系统的DNS服务器，例如切换到 Google 的 DNS (8.8.8.8) 或 Cloudflare 的 DNS (1.1.1.1)。

### 5. 替代下载方式

本脚本已经集成了多种下载方式（requests, urllib, curl），如果所有方法都失败，可以手动下载文件：

1. 手动访问配置文件中的 URL 下载文件
2. 将下载的文件放置在 `temp` 目录中
3. 重新运行脚本，它会跳过下载步骤，直接执行复制操作

或者使用 Python 脚本中的以下替代方法手动下载：

```python
# 方法1: requests
import requests
r = requests.get('URL', stream=True)
with open('file.dat', 'wb') as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)

# 方法2: urllib
import urllib.request
urllib.request.urlretrieve('URL', 'file.dat')
```

## 高级用法

### 自定义下载地址

如果默认的下载地址不可用，您可以修改配置文件中的URL，使用镜像站点或代理服务：

1. 使用 jsdelivr 镜像：将 `testingcf.jsdelivr.net` 替换为 `fastly.jsdelivr.net` 或 `gcore.jsdelivr.net`
2. 使用 GitHub 代理：例如 `https://gh-proxy.com/`, `https://ghproxy.com/` 等

### 手动更新单个文件

如果只有某个文件下载失败，可以手动下载并放入 temp 目录，然后重新运行脚本。 