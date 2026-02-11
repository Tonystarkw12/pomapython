#!/usr/bin/env python3
"""
POMA 2.0 交互式 NMR 仿真脚本
详细显示每一步的输入输出和中间状态
"""

import sys
import os
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

# WolframKernel 路径
KERNEL_PATH = "/home/tony/wolfram/Executables/WolframKernel"

# 设置许可证服务器
os.environ['WOLFRAM_LICENSE_SERVER'] = 'mathematica.tsinghua.edu.cn'


class NMRSimulator:
    """NMR 仿真器类"""

    def __init__(self):
        self.session = None
        self.step_count = 0
        self.history = []

    def connect(self):
        """连接到 Wolfram Kernel"""
        print("🔌 连接到 Wolfram Kernel...")
        self.session = WolframLanguageSession(kernel=KERNEL_PATH)

        # 设置工作目录并加载 POMA
        current_dir = os.path.realpath(os.path.dirname(__file__))
        self.session.evaluate(wlexpr(f'SetDirectory["{current_dir}"]'))
        self.session.evaluate(wlexpr('<<Poma2`'))
        print("✅ 连接成功！POMA 已加载\n")

    def print_separator(self, title=""):
        """打印分隔线"""
        if title:
            print(f"\n{'='*60}")
            print(f"  {title}")
            print(f"{'='*60}\n")
        else:
            print(f"{'-'*60}\n")

    def execute_step(self, description, command, show_input=True, show_output=True):
        """执行一步并显示输入输出"""
        self.step_count += 1

        print(f"📍 步骤 {self.step_count}: {description}")
        print()

        if show_input:
            print("📥 输入命令:")
            print(f"   {command}")
            print()

        # 执行命令
        try:
            result = self.session.evaluate(wlexpr(command))

            if show_output:
                print("📤 输出结果:")
                self.format_output(result)
                print()

            # 保存历史
            self.history.append({
                'step': self.step_count,
                'description': description,
                'command': command,
                'result': str(result)
            })

            return result
        except Exception as e:
            print(f"❌ 错误: {e}")
            return None

    def format_output(self, result):
        """格式化输出结果"""
        result_str = str(result)

        # 如果结果很长，分行显示
        if len(result_str) > 60:
            print("   " + result_str)
        else:
            print(f"   {result_str}")

    def set_parameters(self, params):
        """设置 NMR 参数"""
        self.print_separator("⚙️  设置 NMR 参数")

        for param, value in params.items():
            cmd = f'{param} = {value}'
            self.execute_step(
                f"设置 {param}",
                cmd,
                show_input=False,
                show_output=False
            )
            print(f"   ✅ {param} = {value}")

        print()

    def run_sequence(self, initial_state, steps):
        """运行完整的脉冲序列"""
        self.print_separator("🚀 开始脉冲序列仿真")

        # 显示初始状态
        print("🎯 初始状态:")
        self.format_output(initial_state)
        print()

        # 保存当前状态
        current_state = initial_state
        self.execute_step(
            "初始化自旋系统",
            f'sigma = {initial_state}',
            show_input=False,
            show_output=False
        )

        # 执行每一步
        for step_desc, step_cmd in steps:
            print(f"\n{'─'*60}")
            print(f"⚡ 操作: {step_desc}")
            print(f"{'─'*60}\n")

            print("📝 Wolfram 代码:")
            print(f"   sigma = {step_cmd}[sigma]")
            print()

            # 执行步骤
            current_state = self.session.evaluate(wlexpr(f'{step_cmd}[sigma]'))

            print("📊 当前状态:")
            self.format_output(current_state)
            print()

            # 更新 sigma
            self.session.evaluate(wlexpr('sigma = %s' % current_state))

        self.print_separator("✅ 序列仿真完成")

    def get_observable(self, state=None):
        """获取可观测信号"""
        self.print_separator("📡 可观测信号")

        if state:
            result = self.execute_step(
                "提取可观测磁化",
                f'observable[{state}]',
                show_input=False
            )
        else:
            result = self.execute_step(
                "提取可观测磁化",
                'observable[sigma]',
                show_input=False
            )

        return result

    def show_raiselower(self, state=None):
        """转换为升降算符表示"""
        self.print_separator("⬆️⬇️ 升降算符表示")

        if state:
            result = self.execute_step(
                "转换为升降算符",
                f'raiselower[{state}]',
                show_input=False
            )
        else:
            result = self.execute_step(
                "转换为升降算符",
                'raiselower[sigma]',
                show_input=False
            )

        return result

    def show_summary(self):
        """显示仿真摘要"""
        self.print_separator("📋 仿真摘要")

        print(f"总步骤数: {self.step_count}")
        print(f"历史记录: {len(self.history)} 条\n")

    def disconnect(self):
        """断开连接"""
        if self.session:
            self.session.terminate()
            print("\n👋 已断开 Wolfram Kernel 连接")


def demo_simple_pulse():
    """演示：简单脉冲序列"""
    sim = NMRSimulator()
    sim.connect()

    sim.print_separator("示例 1: 简单的 90° 脉冲序列")

    # 运行序列
    sim.run_sequence(
        initial_state='spin[1,z]',
        steps=[
            ("90° x 脉冲 (作用于自旋 1)", "pulse[90, x, {1}]"),
            ("延迟 0.1 秒", "delay[0.1, {{1,2}}]"),
        ]
    )

    # 转换为升降算符
    sim.show_raiselower()

    # 获取可观测信号
    sim.get_observable()

    # 显示摘要
    sim.show_summary()

    sim.disconnect()


def demo_hsqc():
    """演示：HSQC 脉冲序列"""
    sim = NMRSimulator()
    sim.connect()

    sim.print_separator("示例 2: HSQC (异核单量子相干) 序列")

    # 设置参数
    sim.set_parameters({
        'j[1,2]': 140,    # 1H-X 耦合常数 (Hz)
        'w[1]': 500,       # 1H 拉莫尔频率 (MHz)
        'w[2]': 50,        # X 核拉莫尔频率 (MHz)
    })

    # HSQC 序列步骤
    hsqc_steps = [
        ("90° x 脉冲作用于 1H", "pulse[90, x, {1}]"),
        ("演化 1/(4J) = 1.79 ms", "delay[1/(4*140), {{1,2}}]"),
        ("180° x 脉冲作用于所有自旋", "pulse[180, x]"),
        ("演化 1/(4J) = 1.79 ms", "delay[1/(4*140), {{1,2}}]"),
        ("90° y 脉冲作用于 X 核", "pulse[90, y, {2}]"),
    ]

    # 运行序列
    sim.run_sequence(
        initial_state='spin[1,z] spin[2,z]',
        steps=hsqc_steps
    )

    # 转换为升降算符
    sim.show_raiselower()

    # 获取可观测信号
    sim.get_observable()

    # 显示摘要
    sim.show_summary()

    sim.disconnect()


def demo_custom_sequence():
    """自定义序列演示"""
    sim = NMRSimulator()
    sim.connect()

    sim.print_separator("示例 3: 自定义 COSY 序列")

    # 设置参数
    sim.set_parameters({
        'j[1,2]': 10,     # 同核耦合常数
        'w[1]': 500,       # 自旋1频率
        'w[2]': 500,       # 自旋2频率
    })

    # COSY 序列: 90° - t1 - 90° - acquire
    cosy_steps = [
        ("第一个 90° 脉冲", "pulse[90, x]"),
        ("演化时间 t1", "delay[0.01, {{1,2}}]"),
        ("第二个 90° 脉冲", "pulse[90, x]"),
    ]

    sim.run_sequence(
        initial_state='spin[1,z] spin[2,z]',
        steps=cosy_steps
    )

    sim.get_observable()
    sim.show_summary()
    sim.disconnect()


def main():
    """主函数"""
    print("="*60)
    print("  POMA 2.0 - 交互式 NMR 仿真工具")
    print("="*60)
    print()

    print("请选择要运行的示例:")
    print("  1. 简单的 90° 脉冲序列")
    print("  2. HSQC (异核相关) 序列")
    print("  3. COSY (同核相关) 序列")
    print("  4. 退出")
    print()

    choice = input("请输入选择 (1-4): ").strip()

    if choice == '1':
        demo_simple_pulse()
    elif choice == '2':
        demo_hsqc()
    elif choice == '3':
        demo_custom_sequence()
    elif choice == '4':
        print("👋 再见!")
        return 0
    else:
        print("❌ 无效选择!")
        return 1

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
