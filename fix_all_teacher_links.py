import os
import re

def fix_all_teacher_links():
    templates_dir = "app/templates/teacher"
    
    # جميع الروابط القديمة التي تحتاج إصلاح
    old_patterns = [
        "teacher.lessons_management",
        "teacher.tests_management", 
        "teacher.new_lesson",
        "teacher.edit_lesson",
        "teacher.new_test",
        "teacher.manage_questions",
        "teacher.delete_question",
        "teacher.view_results",
        "teacher.view_students",
        "teacher.dashboard"
    ]
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # استبدال جميع الروابط القديمة
                old_content = content
                for pattern in old_patterns:
                    new_pattern = pattern.replace("teacher.", "teacher.teacher_")
                    content = content.replace(pattern, new_pattern)
                
                # إذا تم تغيير أي شيء، احفظ الملف
                if content != old_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ تم إصلاح: {file_path}")

if __name__ == "__main__":
    fix_all_teacher_links()
    print("🎉 تم إصلاح جميع روابط المدرب!")