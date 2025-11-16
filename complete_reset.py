from app import create_app, db
import os

def complete_reset():
    # احذف ملف قاعدة البيانات إذا موجود
    if os.path.exists('focus_center.db'):
        os.remove('focus_center.db')
        print("🗑️  تم حذف قاعدة البيانات القديمة")
    
    app = create_app()
    
    with app.app_context():
        # حذف جميع الجداول
        db.drop_all()
        
        # إنشاء جميع الجداول من جديد
        db.create_all()
        
        print("✅ تم إنشاء قاعدة البيانات الجديدة بنجاح!")
        print("📊 الجداول المنشأة:")
        print("   - student (الطلاب)")
        print("   - lesson (الدروس) - مع جميع الأعمدة الجديدة")
        print("   - diagnostic_test (الاختبارات) - مع جميع الأعمدة الجديدة") 
        print("   - test_result (النتائج) - مع جميع الأعمدة الجديدة")

if __name__ == "__main__":
    complete_reset()