# mihomo-party 规则文件更新工具

这个工具用于自动下载并更新 mihomo 相关规则文件。支持批处理脚本和 Python 两种运行方式，具有多种下载方式自动切换、详细日志记录等功能。

## 功能特点

- 自动下载以下规则文件：
  - geoip.dat (来自 Loyalsoldier/v2ray-rules-dat)
  - geosite.dat (来自 Loyalsoldier/v2ray-rules-dat)
  - geoip.metadb (来自 MetaCubeX/meta-rules-dat)
  - ASN.mmdb (从 GeoLite2-ASN.mmdb 重命名)
  - country.mmdb (来自 MetaCubeX/meta-rules-dat)
- 多种下载方式自动切换（curl、PowerShell WebClient、BITS、Python requests/urllib）
- 详细的日志记录（按日期分类）
- 自动更新以下目录：
  - `%APPDATA%\mihomo-party\test`
  - `%APPDATA%\mihomo-party\work`
  - `work` 目录下的所有子目录

## 使用方法

### 批处理脚本 (.bat)

直接双击运行 `update_rules_data.bat` 即可。

### Python 脚本 (.py)

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行脚本：
```bash
python update_rules_data.py
```

两种方式都会自动：
1. 创建必要的目录（temp、log）
2. 下载最新的规则文件
3. 更新所有目标目录
4. 记录详细日志

## 配置文件

首次运行时会自动创建配置文件 `config.ini`，包含下载地址配置：

```ini
[URLS]
GEOIP_URL=https://testingcf.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geoip.dat
GEOSITE_URL=https://testingcf.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geosite.dat
GEOIPDB_URL=https://testingcf.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geoip.metadb
ASNDB_URL=https://gh-proxy.com/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/GeoLite2-ASN.mmdb
COUNTRY_URL=https://testingcf.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/country.mmdb
```

可以根据需要修改配置文件中的下载地址。

## 日志记录

- 日志文件保存在 `log` 目录下
- 使用 `YYYY-MM-DD.log` 格式命名
- 同一天的多次运行会追加到同一个日志文件
- 记录内容包括：
  - 下载过程
  - 文件更新状态
  - 错误信息

## 目录结构

```
mihomo-party/
├── update_rules_data.bat    # 批处理主程序
├── update_rules_data.py     # Python主程序
├── requirements.txt         # Python依赖
├── config.ini              # 配置文件
├── temp/                   # 临时文件目录
└── log/                    # 日志目录
    └── YYYY-MM-DD.log     # 日志文件
```

## 故障排除

### 下载失败

如果遇到下载失败，脚本会自动尝试不同的下载方法：

#### 批处理脚本：
1. 首先尝试使用 curl 下载
2. 如果 curl 失败，尝试使用 PowerShell WebClient
3. 如果 WebClient 失败，尝试使用 BITS 传输

#### Python 脚本：
1. 首先尝试使用 requests 库下载
2. 如果 requests 失败，尝试使用 urllib
3. 如果 urllib 失败，尝试使用 curl

可以查看日志文件了解具体失败原因。

### 常见问题解决

1. 网络连接问题
   - 检查网络连接
   - 确认是否可以访问 GitHub
   - 考虑使用代理或镜像站点

2. 权限问题
   - 确保对目标目录有写入权限
   - 检查防火墙设置

3. 文件占用
   - 确保目标文件没有被其他程序占用
   - 关闭可能使用这些文件的程序

4. Python相关问题
   - 确保已安装所需依赖 (`pip install -r requirements.txt`)
   - 检查 Python 版本是否为 3.6+
   - 如遇到 SSL 错误，可能需要更新 Python 的 SSL 证书

## 注意事项

1. 脚本使用 Windows 环境变量 `%APPDATA%` 定位用户配置目录
2. 批处理脚本需要确保系统支持 PowerShell 命令
3. Python 脚本需要 Python 3.6+ 环境
4. 建议定期运行以保持规则文件更新 