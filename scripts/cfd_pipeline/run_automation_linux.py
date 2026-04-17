import os
import csv
import math
from pathlib import Path

# 项目根目录 (scripts/cfd_pipeline/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# 脚本所在目录 (用于定位 fluent_template.jou)
SCRIPT_DIR = Path(__file__).resolve().parent

# ==============================================================================
# --- 用户需要配置的区域 ---
# ==============================================================================

# --- Windows 环境配置 ---
CASES_ROOT_DIR_WINDOWS = r"C:\Users\A\Desktop\klw\simple\simple_files_new"
CSV_FILENAME = str(PROJECT_ROOT / "case.csv")
JOU_TEMPLATE_FILENAME = str(SCRIPT_DIR / "fluent_template.jou")

# --- Linux 环境配置 ---
LINUX_FLUENT_EXEC_COMMAND = "/public3/home/sc71124/software-sc71124/install231/install231/ansys_inc/v231/fluent/bin/fluent"
LINUX_CASES_ROOT_DIR = "/public3/home/sc71124/klw/simple_files_new"
NUM_CORES = 12
CASE_FILENAME = "FFF.1-91.cas.h5"

# --- 输出配置 ---
# 您现在有500个算例，分成3个脚本可能每个脚本跑太久。
# 建议分成 5 个或更多，这里我先设为 5，您可以根据需要改回 3。
NUM_SCRIPTS_TO_GENERATE = 5
OUTPUT_SCRIPT_PREFIX = "run_fluent_part"

# 总算例数量 (dp0 - dp499)
TOTAL_CASE_COUNT = 500


# ==============================================================================
# --- 脚本主程序 ---
# ==============================================================================

def main():
    print(f"开始生成自动化脚本 (目标: {TOTAL_CASE_COUNT} 个算例, 修改Report文件名)...")

    # --- 1. 读取CSV文件 ---
    try:
        with open(CSV_FILENAME, 'r') as f:
            time_steps_list = [row[0].strip() for row in csv.reader(f) if row]
        print(f"成功读取 {len(time_steps_list)} 个时间步数据。")
    except FileNotFoundError:
        print(f"[错误] CSV文件 '{CSV_FILENAME}' 未找到！")
        return

    # --- 2. 读取JOU模板 ---
    try:
        with open(JOU_TEMPLATE_FILENAME, 'r') as f:
            jou_template_content = f.read()
    except FileNotFoundError:
        print(f"[错误] JOU模板 '{JOU_TEMPLATE_FILENAME}' 未找到！")
        return

    # --- 3. 生成命令 ---
    all_commands = []
    num_cases_found = 0

    # 循环范围改为 0 到 499
    for i in range(TOTAL_CASE_COUNT):
        case_name = f"dp{i}"
        win_case_dir = os.path.join(CASES_ROOT_DIR_WINDOWS, case_name)
        win_cas_path = os.path.join(win_case_dir, CASE_FILENAME)

        linux_case_dir = f"{LINUX_CASES_ROOT_DIR}/{case_name}"
        linux_cas_path = f"{linux_case_dir}/{CASE_FILENAME}"
        linux_dat_path = linux_cas_path.replace(".cas.h5", ".dat.h5")

        if os.path.exists(win_cas_path):
            num_cases_found += 1

            # 如果CSV数据不够500行，防止报错
            if i < len(time_steps_list):
                time_steps = time_steps_list[i]
            else:
                print(f"[警告] {case_name} 缺少时间步数据 (CSV行数不足)，跳过。")
                continue

            # --- 定义 Report 输出文件名 ---
            # 最终会在Linux上生成如: dp0_area.out, dp0_report.out
            report_file_area = f"{case_name}_area.out"
            report_file_report = f"{case_name}_report.out"

            # 填充模板
            jou_content = jou_template_content.format(
                case_path=linux_cas_path,
                time_steps=time_steps,
                dat_path=linux_dat_path,
                report_file_area=report_file_area,  # 传入变量
                report_file_report=report_file_report  # 传入变量
            )

            # 写入 .jou 文件
            os.makedirs(win_case_dir, exist_ok=True)
            generated_jou_filename = f"run_{case_name}.jou"
            with open(os.path.join(win_case_dir, generated_jou_filename), 'w') as f:
                f.write(jou_content)

            # 生成 Linux 命令 (不带外层双引号)
            linux_jou_path = f"{linux_case_dir}/{generated_jou_filename}"
            command = f'{LINUX_FLUENT_EXEC_COMMAND} 3ddp -g -t{NUM_CORES} -i {linux_jou_path}'
            all_commands.append((case_name, command))
        else:
            # 仅打印前几个缺失警告，避免刷屏
            if i < 5:
                print(f"[提示] 未找到: {win_cas_path} (若只有部分文件可忽略)")

    print(f"\n共处理了 {num_cases_found} 个有效case。")

    if not all_commands:
        print("[错误] 没有生成任何命令。")
        return

    # --- 4. 生成 .sh 脚本 ---
    total_cases = len(all_commands)
    cases_per_script = math.ceil(total_cases / NUM_SCRIPTS_TO_GENERATE)

    for i in range(NUM_SCRIPTS_TO_GENERATE):
        start_index = i * cases_per_script
        end_index = start_index + cases_per_script
        script_chunk = all_commands[start_index:end_index]

        if not script_chunk: continue

        script_filename = f"{OUTPUT_SCRIPT_PREFIX}_{i + 1}.sh"
        with open(script_filename, 'w', newline='\n') as f:
            f.write("#!/bin/bash\n")
            f.write(f'echo "Starting Part {i + 1}..."\n\n')
            for case_name, cmd in script_chunk:
                f.write(f'echo "[{case_name}] running..."\n')
                f.write(f'{cmd}\n')
                f.write(f'echo "[{case_name}] done."\n\n')

        print(f"已生成: {script_filename} ({len(script_chunk)} 个算例)")

    print("\n--- 完成 ---")
    print("请上传新的 .sh 文件到 Linux，并记得运行 'dos2unix *.sh'！")


if __name__ == '__main__':
    main()