#!/usr/bin/env python3
"""
POMA 2.0 运行脚本
使用 wolframclient Python 库运行 Mathematica 包
"""

import sys
import os
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

# WolframKernel 路径
KERNEL_PATH = "/home/tony/wolfram/Executables/WolframKernel"

# 设置许可证服务器
os.environ['WOLFRAM_LICENSE_SERVER'] = 'mathematica.tsinghua.edu.cn'

def main():
    print("=" * 60)
    print("POMA 2.0 - NMR Product Operator Formalism")
    print("=" * 60)
    print()

    # 获取当前目录
    current_dir = os.path.realpath(os.path.dirname(__file__))

    print(f"当前目录: {current_dir}")
    print(f"WolframKernel: {KERNEL_PATH}")
    print()

    try:
        # 创建会话
        print("正在连接 Wolfram Kernel...")
        session = WolframLanguageSession(kernel=KERNEL_PATH)
        print("✓ 连接成功!\n")

        # 设置工作目录
        print(f"设置工作目录: {current_dir}")
        session.evaluate(wlexpr(f'SetDirectory["{current_dir}"]'))

        # 加载 POMA 包
        print("\n正在加载 Poma2.m...")
        result = session.evaluate(wlexpr('<<Poma2`'))
        print("✓ POMA 包加载成功!\n")

        # 显示可用命令
        print("-" * 50)
        print("查询 POMA 命令列表...")
        commands = session.evaluate(wlexpr('?commands'))
        print(commands)
        print()

        # 运行示例 1: 简单的脉冲序列
        print("-" * 50)
        print("示例 1: 简单的 90度 x 脉冲序列")
        print("-" * 50)

        print("\n1. 初始状态: spin[1,z]")
        sigma0 = session.evaluate(wlexpr('spin[1,z]'))
        print(f"   结果: {sigma0}")

        print("\n2. 应用 90度 x 脉冲...")
        sigma1 = session.evaluate(wlexpr('pulse[90, x][spin[1,z]]'))
        print(f"   结果: {sigma1}")

        print("\n3. 转换为升降算符表示:")
        sigma_rl = session.evaluate(wlexpr('raiselower[pulse[90, x][spin[1,z]]]'))
        print(f"   结果: {sigma_rl}")

        # 运行示例 2: HSQC 脉冲序列
        print("\n" + "=" * 50)
        print("示例 2: 运行 HSQC 示例")
        print("=" * 50)

        print("\n正在加载 HSQC.m...")
        try:
            # 设置耦合常数
            print("设置参数...")
            session.evaluate(wlexpr('j[1,2] = 140'))
            session.evaluate(wlexpr('w[1] = 500'))
            session.evaluate(wlexpr('w[2] = 50'))

            print("✓ 参数设置完成")
            print()
            print("提示: 完整的 HSQC 示例请查看 HSQC.m 文件")

        except Exception as e:
            print(f"注意: {e}")

        print("\n" + "=" * 50)
        print("运行完成!")
        print("=" * 50)

        # 关闭会话
        session.terminate()

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
