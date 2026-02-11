# 🧬 POMA Python - NMR 脉冲序列仿真工具

<div align="center">

**Python 接口 + Wolfram Engine POMA 2.0**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Wolfram](https://img.shields.io/badge/Wolfram-14.2.1-red)](https://www.wolfram.com/)
[![License](https://img.shields.io/badge/License-POMA%202.0-green)](./LICENSE)

用 Python 探索 NMR 脉冲序列的奥秘

[快速开始](#-快速开始) • [功能](#-核心功能) • [示例](#-使用示例) • [文档](#-文档)

</div>

---

## 📖 简介

**POMA Python** 是对经典 POMA 2.0 (Product Operator Formalism) Mathematica 包的 Python 封装。它提供了友好的 Python 接口来仿真 NMR 脉冲序列，特别适合：

- 🧪 **NMR 研究** - 快速验证脉冲序列设计
- 📚 **教学演示** - 清晰展示每一步的物理过程
- 🔬 **学习工具** - 理解产品算符形式体系
- 📊 **数据分析** - 集成到 Python 工作流

### 特点

✨ **多种运行模式**
- 🚀 交互式 REPL 快速测试
- 📊 详细演示模式学习序列
- 🎨 美化输出用于报告
- 🔧 纯 Wolfram Language 支持

🎯 **用户友好**
- 清晰的输入输出显示
- Unicode 数学符号
- 预设的经典序列示例
- 完整的中文文档

⚡ **易于使用**
```python
from run_poma_interactive import NMRSimulator

sim = NMRSimulator()
sim.connect()
sim.run_sequence('spin[1,z]', [
    ("90°x 脉冲", "pulse[90,x]"),
    ("延迟", "delay[0.1]"),
])
```

---

## 🚀 快速开始

### 前置要求

1. **Wolfram Engine 14.2+**
   - 下载: https://www.wolfram.com/engine/
   - 或使用网络许可证服务器

2. **Python 3.8+**
```bash
# 使用 conda
conda create -n wolfram python=3.10
conda activate wolfram

# 安装依赖
pip install wolframclient
```

3. **POMA 2.0 包**
   - 已包含在本项目的 `poma-2.0/` 目录
   - 或从原项目获取

### 配置许可证

**方式 1: 网络许可证（推荐）**
```bash
# 创建许可证配置
mkdir -p ~/.Wolfram/Licensing
echo '!mathematica.tsinghua.edu.cn' > ~/.Wolfram/Licensing/mathpass
```

**方式 2: 本地许可证**
按照 Wolfram 官方指引激活

### 运行示例

```bash
# 克隆仓库
git clone https://github.com/yourusername/pomapython.git
cd pomapython

# 运行交互式演示
python run_poma_interactive.py
```

---

## 🎯 核心功能

### 1. 快速 REPL (`quick_run.py`)

⚡ 即时执行 POMA 代码，查看结果

```bash
$ python quick_run.py
>>> pulse[90,x][spin[1,z]]
📤 -I1y

>>> j[1,2]=140; w[1]=500
✅ 参数已设置
```

**适用:** 快速测试、代码调试

---

### 2. 详细演示 (`run_poma_interactive.py`)

📊 显示每一步的完整输入输出

```bash
$ python run_poma_interactive.py
请选择示例 (1-3): 2

============================================================
  🚀 HSQC 脉冲序列仿真
============================================================

📍 步骤 1: 90°x 脉冲作用于 1H
📝 代码: sigma = pulse[90, x, {1}][sigma]
📊 结果: -I1y I2z

📍 步骤 2: 演化时间 τ = 1/(4J)
📝 代码: sigma = delay[1/(4*140), {{1,2}}][sigma]
📊 结果: <详细展开>
```

**适用:** 学习理解、教学演示

---

### 3. 美化输出 (`run_poma_beautiful.py`)

🎨 使用 Unicode 和 LaTeX 风格

```bash
$ python run_poma_beautiful.py
选择 (1-3): 2

══════════════════════════════════════════════════════
  🧬 HSQC 脉冲序列
══════════════════════════════════════════════════════

🎯 初始状态: σ₀ = I1z I2z
📐 J₁₂ = 140 Hz, ω₁ = 500 MHz

────────────────────────────────────────────────────────
  步骤 1: 90°x 脉冲
────────────────────────────────────────────────────────
   σ = -I1y I2z
```

**适用:** 报告生成、演示文稿

---

## 💡 使用示例

### 示例 1: 简单的 90° 脉冲

```python
from run_poma_interactive import NMRSimulator

sim = NMRSimulator()
sim.connect()

# 运行序列
sim.run_sequence(
    initial_state='spin[1,z]',
    steps=[
        ("90° x 脉冲", "pulse[90, x]"),
        ("延迟 0.1 秒", "delay[0.1]"),
    ]
)

# 查看可观测信号
sim.get_observable()
sim.disconnect()
```

**输出:**
```
初始状态: I1z
90° x 脉冲 → -I1y
延迟 → -(I1y·cos(0.1·ω₁)) + I1x·sin(0.1·ω₁)
```

---

### 示例 2: HSQC 序列

**Heteronuclear Single Quantum Coherence**

```python
sim = NMRSimulator()
sim.connect()

# 设置参数
sim.set_parameters({
    'j[1,2]': 140,    # 1H-X 耦合 (Hz)
    'w[1]': 500,       # 1H 频率 (MHz)
    'w[2]': 50,        # X 核频率 (MHz)
})

# HSQC 序列
hsqc_steps = [
    ("90°x(¹H)", "pulse[90, x, {1}]"),
    ("τ=1/(4J)", "delay[1/(4*140), {{1,2}}]"),
    ("180°x", "pulse[180, x]"),
    ("τ=1/(4J)", "delay[1/(4*140), {{1,2}}]"),
    ("90°y(X)", "pulse[90, y, {2}]"),
]

sim.run_sequence('spin[1,z] spin[2,z]', hsqc_steps)
sim.final_observable()
sim.disconnect()
```

**物理过程:**
```
I1zI2z → [-I1y]I2z → [演化相干] → [180°重聚焦]
→ [演化] → -I1yI2x → 双量子相干
```

---

## 📚 POMA 命令参考

### 脉冲 (Pulse)

```wolfram
pulse[angle, phase]              # 作用于所有自旋
pulse[angle, phase, {1}]         # 仅自旋 1
pulse[angle, phase, {1,2}]       # 自旋 1 和 2
pulse[90, x]                    # 90 度 x 脉冲
pulse[180, y, {1}]             # 180 度 y 脉冲（自旋1）
```

### 延迟 (Delay)

```wolfram
delay[t]                        # 仅化学位移
delay[t, {{1,2}}]              # 化学位移 + J 耦合
delay[t, {{1,2}}, {1}]         # 仅自旋1有化学位移
delay[1/(4*140), {{1,2}}]      # τ = 1/(4J) 演化
```

### 可观测 (Observable)

```wolfram
observable[sigma]                # 提取横向磁化
raiselower[sigma]               # 转升降算符
cartesian[sigma]                # 转笛卡尔算符
```

### 参数 (Parameters)

```wolfram
j[1,2] = 140                  # J 耦合常数 (Hz)
w[1] = 500                    # 拉莫尔频率 (MHz)
g[1] = 26.752                 # 旋磁比 (MHz/T)
nucleus[1] = "H"              # 核素符号
```

---

## 📂 项目结构

```
pomapython/
├── README.md                    # 本文档
├── README_CN.md                # 中文完整指南
├── SCRIPTS_GUIDE.md            # 脚本选择指南
│
├── quick_run.py               # [推荐] 快速 REPL
├── run_poma_interactive.py    # 详细演示版
├── run_poma_beautiful.py      # 美化输出版
├── run_poma_v2.py            # 基础版本
│
└── poma-2.0/                # POMA 核心包
    ├── Poma2.m
    ├── HSQC.m
    ├── 3QF-COSY.m
    └── ...
```

---

## 🛠️ 高级用法

### 自定义序列研究

创建你自己的实验脚本：

```python
#!/usr/bin/env python3
from run_poma_interactive import NMRSimulator

def my_experiment():
    sim = NMRSimulator()
    sim.connect()

    # 你的实验参数
    sim.set_parameters({
        'j[1,2]': 10,
        'w[1]': 600,
        'w[2]': 150,
    })

    # 定义新序列
    tocsy_steps = [
        ("90° 脉冲", "pulse[90, x]"),
        ("自旋锁定", "delay[0.05, {{1,2}}]"),
        ("混合脉冲", "pulse[180, y]"),
        ("检测", "observable"),
    ]

    sim.run_sequence('spin[1,z] spin[2,z]', tocsy_steps)
    sim.disconnect()

if __name__ == "__main__":
    my_experiment()
```

### 集成到科学计算工作流

```python
import numpy as np
import matplotlib.pyplot as plt
from run_poma_interactive import NMRSimulator

# 系统性研究 J 耦合的影响
sim = NMRSimulator()
sim.connect()

j_values = np.linspace(50, 200, 10)
results = []

for j_val in j_values:
    sim.execute('', f'j[1,2] = {j_val}', show_state=False)
    # 运行序列，记录结果
    # ...
    sim.execute('', 'ClearAll[j]', show_state=False)

sim.disconnect()

# 绘图分析
plt.plot(j_values, results)
plt.xlabel('J Coupling (Hz)')
plt.ylabel('Signal Intensity')
plt.show()
```

---

## 📖 参考文献

**POMA 原始论文:**
```
Güntert, P., Schäfer, N., Otting, G. & Wüthrich, K. (1993)
POMA: a complete Mathematica implementation of the NMR product
operator formalism.
Journal of Magnetic Resonance A 101, 103-105.
```

**产品算符理论:**
```
Sørensen, O.W. et al. (1983)
Progress in NMR Spectroscopy 16, 163-192.
```

---

## 🐛 故障排除

### WolframKernel 未找到

```bash
# 检查路径
which WolframKernel

# 如果未找到，添加到 PATH
export PATH=/path/to/wolfram/Executables:$PATH

# 或在脚本中设置
KERNEL_PATH = "/path/to/WolframKernel"
```

### 许可证错误

```bash
# 检查许可证文件
cat ~/.Wolfram/Licensing/mathpass

# 手动配置网络许可证
export WOLFRAM_LICENSE_SERVER=mathematica.tsinghua.edu.cn
```

### Python 连接失败

```bash
# 检查 wolframclient
pip list | grep wolfram

# 重新安装
pip install --upgrade wolframclient

# 测试连接
python -c "from wolframclient.evaluation import WolframLanguageSession"
```

---

## 🤝 贡献

欢迎贡献！请：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

**贡献方向:**
- 🆕 新的脉冲序列示例
- 🐛 Bug 修复
- 📚 文档改进
- ✨ 功能增强

---

## 📄 许可证

本软件遵循 **POMA 2.0 许可证**。详见 [LICENSE](./LICENSE) 文件。

核心要点：
- ✅ 学术研究使用
- ✅ 机构内部使用
- ❌ 商业分发需授权
- 📖 引用请使用原始论文

---

## 📞 联系方式

- **Issues:** [GitHub Issues](https://github.com/yourusername/pomapython/issues)
- **Email:** (your email)

---

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star！

---

<div align="center">

**用 Python 探索 NMR 的无限可能** 🧬⚡

Made with ❤️ by NMR enthusiasts

</div>
