import json

# 变量gl_config: 全局配置文件
print("加载配置文件中...")
with open("config.json", "r") as f:
    gl_config = json.load(f)
print(f"配置文件信息：{gl_config}")
