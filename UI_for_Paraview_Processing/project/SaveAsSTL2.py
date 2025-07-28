from paraview.simple import *
import os

# 获取用户输入的保存文件夹路径
save_folder = input("请输入保存文件夹路径（例如 E:/your_folder/）：")

# 确保路径合法（防止输入时漏掉反斜杠）
if not save_folder.endswith('/') and not save_folder.endswith('\\'):
    save_folder += '/'

# 获取所有当前的源
sources = GetSources()

# 按名字筛选以 Contour_ 开头的对象
contour_sources = [(key, FindSource(key[0])) for key in sources if key[0].startswith("Contour_")]

# 如果没有找到任何 Contour_XX 的对象
if not contour_sources:
    print("未找到任何命名为 Contour_XX 的对象。")
else:
    # 批量保存
    for key, obj in contour_sources:
        SetActiveSource(obj)
        filename = f"{key[0]}.stl"
        full_path = os.path.join(save_folder, filename)
        SaveData(full_path, proxy=obj)
        print(f"已保存：{full_path}")
