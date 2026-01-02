"""
此文件阻止 agno/ 目录被 Python 当作命名空间包。

真正的 agno 包在 agno/libs/agno/ 中，已通过 pip install -e 安装到虚拟环境。

如果你看到此错误，说明导入路径有问题。请检查：
1. agno 是否已正确安装：pip show agno
2. Python 的 sys.path 是否包含了项目根目录（不应该）
"""
raise ImportError(
    "请勿从子模块目录导入 agno。\n"
    "agno 包已通过 'pip install -e agno/libs/agno/' 安装在虚拟环境中。\n"
    "如果遇到此错误，请检查 PYTHONPATH 和 sys.path 配置。"
)

