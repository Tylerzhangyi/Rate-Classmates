#!/usr/bin/env python3
"""
导入学生数据脚本
从Excel文件导入云谷学校的学生数据到数据库
"""
import os
import sys
import django
import pandas as pd

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import School, Student

# 年级映射：年级名称 -> grade值
GRADE_MAPPING = {
    '预备十年级': 2025,
    '十年级': 2024,
    '十一年级': 2023,
    '十二年级': 2022,
}

def import_students(excel_path):
    """从Excel文件导入学生数据"""
    # 读取Excel文件
    print(f"正在读取Excel文件: {excel_path}")
    df = pd.read_excel(excel_path)
    
    # 检查必要的列
    required_columns = ['姓名', '年级']
    for col in required_columns:
        if col not in df.columns:
            print(f"错误: Excel文件中缺少必要的列: {col}")
            return
    
    # 获取杭州云谷学校（必须已存在，不创建新学校）
    school_name = '杭州云谷学校'
    school = School.objects.filter(school_name=school_name).first()
    if not school:
        print(f"错误: 找不到学校 '{school_name}'")
        print("请确保该学校已存在于数据库中")
        return
    print(f"使用学校: {school_name}")
    
    # 统计信息
    total_count = 0
    success_count = 0
    skip_count = 0
    error_count = 0
    
    # 遍历每一行数据
    print("\n开始导入学生数据...")
    for index, row in df.iterrows():
        total_count += 1
        name = str(row['姓名']).strip()
        grade_text = str(row['年级']).strip()
        
        # 跳过空姓名
        if not name or name == 'nan':
            skip_count += 1
            continue
        
        # 转换年级
        if grade_text not in GRADE_MAPPING:
            print(f"警告: 第{index+2}行，未知年级 '{grade_text}'，跳过")
            skip_count += 1
            continue
        
        grade = GRADE_MAPPING[grade_text]
        
        # 检查学生是否已存在（同一学校、同一姓名、同一年级）
        existing = Student.objects.filter(
            school=school,
            name=name,
            grade=grade
        ).first()
        
        if existing:
            print(f"跳过: {name} ({grade_text}, grade={grade}) 已存在")
            skip_count += 1
            continue
        
        # 创建新学生
        try:
            student = Student.objects.create(
                school=school,
                name=name,
                grade=grade
            )
            success_count += 1
            if success_count % 10 == 0:
                print(f"已导入 {success_count} 名学生...")
        except Exception as e:
            print(f"错误: 导入 {name} ({grade_text}) 时出错: {e}")
            error_count += 1
    
    # 打印统计信息
    print("\n" + "="*50)
    print("导入完成！")
    print(f"总计: {total_count} 行")
    print(f"成功: {success_count} 名学生")
    print(f"跳过: {skip_count} 行（已存在或数据无效）")
    print(f"错误: {error_count} 行")
    print("="*50)

if __name__ == '__main__':
    # Excel文件路径（相对于项目根目录）
    excel_path = '../2025高中名单 (2).xlsx'
    
    if not os.path.exists(excel_path):
        print(f"错误: 找不到Excel文件: {excel_path}")
        print("请确保文件路径正确")
        sys.exit(1)
    
    import_students(excel_path)

