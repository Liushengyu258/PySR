import os
import pandas as pd

# 1. 设置文件夹路径 (注意前面的 r 是为了防止转义字符报错)
folder_path = r"C:\Users\A\Desktop\klw\simple\data"

# 2. 定义列标题 (根据你提供的内容整理)
columns = [
    "Time Step", "area",  "flow-time"
]

data_list = []
index_labels = []

print("开始处理文件...")

# 3. 循环遍历 dp0 到 dp999
for i in range(500):
    filename = f"dp{i}_area.out"
    file_full_path = os.path.join(folder_path, filename)

    # 行标题，如 dp0, dp1...
    row_label = f"dp{i}"

    if os.path.exists(file_full_path):
        try:
            with open(file_full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                # 获取最后一行并去除首尾空白符
                last_line = lines[-1].strip()

                # 如果文件最后一行是空的，尝试往前找一行
                if not last_line and len(lines) > 1:
                    last_line = lines[-2].strip()

                if last_line:
                    # 根据空格分割数据
                    values = last_line.split()

                    # 简单检查数据长度是否匹配列数（可选，仅作提示）
                    if len(values) != len(columns):
                        print(f"警告: {filename} 数据列数 ({len(values)}) 与标题列数 ({len(columns)}) 不一致。")

                    data_list.append(values)
                    index_labels.append(row_label)
                else:
                    print(f"警告: {filename} 文件内容为空。")
                    # 依然添加一行空数据或全0，保持行号对齐，或者选择跳过
                    data_list.append([None] * len(columns))
                    index_labels.append(row_label)

        except Exception as e:
            print(f"读取 {filename} 出错: {e}")
    else:
        print(f"文件未找到: {filename}")
        # 如果文件缺失，可以选择跳过或者填充空值，这里选择不添加到列表中
        # 如果需要强制保留 dp 行号，可以取消下面两行的注释
        # data_list.append([None] * len(columns))
        # index_labels.append(row_label)

# 4. 创建 DataFrame
df = pd.DataFrame(data_list, columns=columns, index=index_labels)

# 5. 导出为 CSV
output_file = str(PROJECT_ROOT / "summary_dp0_499.csv")
df.to_csv(output_file, encoding='utf-8-sig')

print(f"处理完成！文件已保存至: {output_file}")