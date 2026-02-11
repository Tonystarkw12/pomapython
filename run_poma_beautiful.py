#!/usr/bin/env python3
"""
POMA 2.0 美化版 NMR 仿真脚本
使用 LaTeX 风格和 Unicode 符号显示 NMR 过程
"""

import sys
import os
import re
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

# WolframKernel 路径
KERNEL_PATH = "/home/tony/wolfram/Executables/WolframKernel"
os.environ['WOLFRAM_LICENSE_SERVER'] = 'mathematica.tsinghua.edu.cn'


class NMRBeautifulOutput:
    """美化 NMR 输出"""

    def __init__(self):
        self.session = None
        self.step = 0

        # POMA 符号到 Unicode 的映射
        self.symbol_map = {
            'spin[': 'I',
            ', x]': 'x',
            ', y]': 'y',
            ', z]': 'z',
            ', plus]': '⁺',
            ', minus]': '⁻',
            'Poma`': '',
            'Times[-1,': '-',
            'Times[': '',
            'Power[2, Rational[-1, 2]]': '½',
            'Rational[1, 2]': '½',
            'Rational[1, 4]': '¼',
            'Plus[': '(',
            ']': ')',
            'Times[Complex[0,': '',
            'Rational[': '',
            '],': ',',
            'Power[': '^',
            'Sin[': 'sin(',
            'Cos[': 'cos(',
            'w[': 'ω',
            '],': ')',
        }

    def connect(self):
        """连接到 Wolfram"""
        print("🔌 正在连接 Wolfram Kernel...")
        self.session = WolframLanguageSession(kernel=KERNEL_PATH)
        current_dir = os.path.realpath(os.path.dirname(__file__))
        self.session.evaluate(wlexpr(f'SetDirectory["{current_dir}"]'))
        self.session.evaluate(wlexpr('<<Poma2`'))
        print("✅ 已连接！POMA 2.0 已加载\n")

    def header(self, text, width=70):
        """打印标题"""
        print(f"\n{'='*width}")
        print(f"  {text}")
        print(f"{'='*width}\n")

    def section(self, text):
        """打印小节标题"""
        print(f"\n{'─'*70}")
        print(f"  {text}")
        print(f"{'─'*70}\n")

    def format_math(self, expr):
        """格式化数学表达式"""
        # 获取 Mathematica 的格式化输出
        try:
            formatted = self.session.evaluate(wlexpr(f'ToString[TeXForm[{expr}]]'))
            return formatted
        except:
            # 如果失败，返回简化格式
            return self.simplify_format(str(expr))

    def simplify_format(self, s):
        """简化的格式化"""
        s = str(s)
        # 移除 Poma` 前缀
        s = s.replace("Poma`", "")
        # 简化一些常见模式
        s = s.replace("spin[", "I")
        s = s.replace(", x]", "x")
        s = s.replace(", y]", "y")
        s = s.replace(", z]", "z")
        s = s.replace(", plus]", "+")
        s = s.replace(", minus]", "-")
        return s

    def execute(self, desc, code, show_state=True):
        """执行命令并显示结果"""
        self.step += 1

        print(f"📍 步骤 {self.step}: {desc}")
        print(f"   💻 代码: {code}")
        print()

        result = self.session.evaluate(wlexpr(code))

        if show_state:
            # 获取 Mathematica 格式化的输出
            try:
                pretty_output = self.session.evaluate(
                    wlexpr(f'ToString[InputForm[{result}]]')
                )
                # 移除多余引号
                pretty_output = pretty_output.strip('"')
                print(f"   📊 结果: {pretty_output}")
            except:
                print(f"   📊 结果: {self.simplify_format(result)}")

        print()
        return result

    def pulse_sequence(self, title, initial_state, steps):
        """运行脉冲序列"""
        self.header(f"🧬 {title}")

        print("🎯 初始状态:")
        print(f"   σ₀ = {self.simplify_format(initial_state)}\n")

        # 初始化
        current = f"sigma = {initial_state}"
        self.session.evaluate(wlexpr(current))

        # 显示参数（如果有）
        try:
            j_val = self.session.evaluate(wlexpr('j[1,2]'))
            if j_val:
                print("📐 参数设置:")
                print(f"   J₁₂ = {j_val} Hz")

            w1 = self.session.evaluate(wlexpr('w[1]'))
            w2 = self.session.evaluate(wlexpr('w[2]'))
            if w1 and w2:
                print(f"   ω₁  = {w1} MHz")
                print(f"   ω₂  = {w2} MHz")
            print()
        except:
            pass

        # 执行每一步
        for i, (op_name, op_code) in enumerate(steps, 1):
            self.section(f"步骤 {i}: {op_name}")

            print(f"   操作: sigma = {op_code}[sigma]")
            print()

            # 执行操作
            current = self.session.evaluate(wlexpr(f'{op_code}[sigma]'))
            self.session.evaluate(wlexpr('sigma = %s' % current))

            # 显示结果
            try:
                pretty = self.session.evaluate(
                    wlexpr('ToString[InputForm[sigma]]')
                )
                pretty = pretty.strip('"')

                # 简化显示
                simple = self.simplify_format(pretty)

                if len(simple) > 70:
                    print(f"   σ = ")
                    print(f"      {simple}")
                else:
                    print(f"   σ = {simple}")
            except Exception as e:
                print(f"   σ = {current}")

            print()

        self.header("✅ 序列完成")

    def final_observable(self):
        """获取最终可观测信号"""
        self.header("📡 可观测信号")

        result = self.session.evaluate(wlexpr('observable[sigma]'))
        print(f"   可观测磁化:")
        print(f"   Mobs = {self.simplify_format(result)}\n")

        # 转换为升降算符
        self.header("⬆️⬇️ 升降算符表示")

        rl = self.session.evaluate(wlexpr('raiselower[sigma]'))
        print(f"   σ(升降算符) = {self.simplify_format(rl)}\n")

    def close(self):
        """关闭连接"""
        if self.session:
            self.session.terminate()
            print("👋 连接已关闭\n")


def demo_hsqc():
    """HSQC 演示"""
    sim = NMRBeautifulOutput()
    sim.connect()

    # 设置参数
    print("⚙️  设置参数:")
    sim.execute("设置耦合常数 J₁₂", 'j[1,2] = 140', show_state=False)
    sim.execute("设置频率 ω₁", 'w[1] = 500', show_state=False)
    sim.execute("设置频率 ω₂", 'w[2] = 50', show_state=False)
    print()

    # HSQC 序列
    steps = [
        ("90°x 脉冲作用于 ¹H", "pulse[90, x, {1}]"),
        ("演化时间 τ = 1/(4J)", "delay[1/(4*140), {{1,2}}]"),
        ("180°x 脉冲作用于所有自旋", "pulse[180, x]"),
        ("演化时间 τ = 1/(4J)", "delay[1/(4*140), {{1,2}}]"),
        ("90°y 脉冲作用于 X 核", "pulse[90, y, {2}]"),
    ]

    sim.pulse_sequence("HSQC 脉冲序列", "spin[1,z] spin[2,z]", steps)
    sim.final_observable()
    sim.close()


def demo_simple():
    """简单演示"""
    sim = NMRBeautifulOutput()
    sim.connect()

    steps = [
        ("90°x 脉冲", "pulse[90, x]"),
        ("延迟 0.1 秒", "delay[0.1]"),
    ]

    sim.pulse_sequence("简单脉冲序列", "spin[1,z]", steps)
    sim.final_observable()
    sim.close()


def main():
    print("="*70)
    print("  🧪 POMA 2.0 - NMR 脉冲序列仿真 (美化版)")
    print("="*70)
    print()

    print("📋 可用示例:")
    print("   1️⃣  简单的 90° 脉冲序列")
    print("   2️⃣  HSQC (异核单量子相干) 序列")
    print("   3️⃣  退出")
    print()

    try:
        choice = input("请选择 (1-3): ").strip()

        if choice == '1':
            demo_simple()
        elif choice == '2':
            demo_hsqc()
        elif choice == '3':
            print("👋 再见!")
            return 0
        else:
            print("❌ 无效选择")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        return 1
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
