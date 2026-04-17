import os
import shutil

# --- 配置路径 ---

# 1. 源文件夹的基础路径 (包含所有 dpX 文件夹的地方)
# 注意：请确保路径中的反斜杠'\'是双写的'\\'或者在字符串前加上r
source_base_dir = r"C:\Users\A\Desktop\klw\simple\simple_files"

# 2. 目标文件夹的基础路径 (脚本会自动创建这个文件夹)
destination_base_dir = r"C:\Users\A\Desktop\klw\simple\simple_files_new"

# 3. 要查找的文件名
file_name = "FFF.1-91.cas.h5"


# --- 脚本主逻辑 ---

def organize_files():
    """
    整理文件，将深层目录中的文件复制到新的、更扁平的目录结构中。
    """
    print("脚本开始执行...")
    print(f"源文件夹: {source_base_dir}")
    print(f"目标文件夹: {destination_base_dir}")

    # 检查源文件夹是否存在
    if not os.path.exists(source_base_dir):
        print(f"错误：源文件夹 '{source_base_dir}' 不存在。请检查路径是否正确。")
        return

    # 创建目标文件夹 (如果不存在)
    os.makedirs(destination_base_dir, exist_ok=True)
    print("目标文件夹已创建或已存在。")

    copied_files_count = 0

    # 循环遍历 dp0 到 dp99 的文件夹
    for i in range(500):
        dp_folder_name = f"dp{i}"

        # 构建完整的文件源路径
        # 例如: C:\Users\A\Desktop\klw\simple\simple_files\dp0\FFF\Fluent\FFF.1-85.cas.h5
        source_file_path = os.path.join(source_base_dir, dp_folder_name, "FFF", "Fluent", file_name)

        # 检查源文件是否存在
        if os.path.exists(source_file_path):

            # 构建目标文件夹路径
            # 例如: C:\Users\A\Desktop\klw\simple\simple_files_new\dp0
            destination_dp_folder = os.path.join(destination_base_dir, dp_folder_name)
            os.makedirs(destination_dp_folder, exist_ok=True)

            # 构建完整的目标文件路径
            # 例如: C:\Users\A\Desktop\klw\simple\simple_files_new\dp0\FFF.1-85.cas.h5
            destination_file_path = os.path.join(destination_dp_folder, file_name)

            try:
                # 复制文件
                print(f"正在复制: {source_file_path} -> {destination_file_path}")
                shutil.copy2(source_file_path, destination_file_path)  # copy2 会同时复制元数据
                copied_files_count += 1
            except Exception as e:
                print(f"复制文件 {source_file_path} 时出错: {e}")

    print("\n--------------------")
    print(f"脚本执行完毕！")
    print(f"总共成功复制了 {copied_files_count} 个文件。")
    print(f"所有文件已保存到: {destination_base_dir}")
    print("--------------------")


# --- 运行脚本 ---
if __name__ == "__main__":
    organize_files()