#!/usr/bin/env python3
"""
POMA 2.0 快速运行脚本
输入任意 Wolfram/POMA 代码，立即查看结果
"""

import sys
import os
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wlexpr

# 配置
KERNEL_PATH = "/home/tony/wolfram/Executables/WolframKernel"
os.environ['WOLFRAM_LICENSE_SERVER'] = 'mathematica.tsinghua.edu.cn'

def print_banner():
    print("="*70)
    print("  ⚡ POMA 2.0 快速运行")
    print("  输入 Wolfram 代码，立即查看结果")
    print("="*70)
    print()

def simplify_output(result):
    """简化输出显示"""
    s = str(result)
    # 简化符号
    s = s.replace("Poma`", "")
    s = s.replace("spin[", "I")
    s = s.replace(", x]", "x")
    s = s.replace(", y]", "y")
    s = s.replace(", z]", "z")
    s = s.replace(", plus]", "+")
    s = s.replace(", minus]", "-")
    return s

def main():
    print_banner()

    # 连接
    print("🔌 连接 Wolfram...")
    session = WolframLanguageSession(kernel=KERNEL_PATH)

    # 加载 POMA
    current_dir = os.path.dirname(os.path.abspath(__file__))
    session.evaluate(wlexpr(f'SetDirectory["{current_dir}"]'))
    session.evaluate(wlexpr('<<Poma2`'))
    print("✅ 已就绪！\n")

    print("💡 提示:")
    print("   - 输入 'help' 查看示例")
    print("   - 输入 'quit' 或 'exit' 退出")
    print("   - 支持多行输入（以空行结束）")
    print()

    # REPL 循环
    while True:
        try:
            print(">>> ", end='', flush=True)

            # 读取输入（可能多行）
            lines = []
            while True:
                line = sys.stdin.readline()
                if not line:  # EOF
                    print()
                    return 0
                if line.strip() == '' and lines:
                    break
                lines.append(line)

            code = ''.join(lines).strip()

            if not code:
                continue

            # 处理特殊命令
            if code.lower() in ('quit', 'exit', 'q'):
                print("👋 再见!")
                break

            if code.lower() == 'help':
                print_help()
                continue

            if code.lower() == 'reset':
                session.evaluate(wlexpr('<<Poma2`'))
                print("✅ POMA 已重置\n")
                continue

            # 执行代码
            print()
            try:
                result = session.evaluate(wlexpr(code))

                # 显示结果
                output = simplify_output(result)
                if len(output) > 100:
                    print("📤 结果:")
                    for line in output.split(','):
                        print(f"   {line.strip()}")
                else:
                    print(f"📤 {output}")
                print()

            except Exception as e:
                print(f"❌ 错误: {e}\n")

        except KeyboardInterrupt:
            print("\n\n使用 'quit' 退出\n")
            continue

    session.terminate()
    return 0

def print_help():
    """打印帮助信息"""
    print()
    print("📚 示例代码:")
    print()
    print("1. 基本脉冲:")
    print("   pulse[90, x][spin[1,z]]")
    print()
    print("2. 序列仿真:")
    print("   sigma = spin[1,z];")
    print("   sigma = pulse[90, x][sigma];")
    print("   sigma = delay[0.1][sigma];")
    print("   sigma")
    print()
    print("3. 设置参数:")
    print("   j[1,2] = 140")
    print("   w[1] = 500")
    print()
    print("4. 查看命令:")
    print("   ?commands")
    print()
    print("5. 可观测信号:")
    print("   observable[spin[1,x]]")
    print()
    print("6. 升降算符:")
    print("   raiselower[spin[1,x]]")
    print()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)
