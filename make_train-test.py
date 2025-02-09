import os
import shutil
import random

# مسیرهای اصلی
base_dir = r"C:\Users\mmras\OneDrive\Desktop\facial regognation Elastic"
source_dir = os.path.join(base_dir, "people_JSONs")
output_dir = os.path.join(base_dir, "people_JSONs_train-test")

# مسیرهای خروجی
train_dir = os.path.join(output_dir, "train")
test_dir = os.path.join(output_dir, "test")

# ایجاد دایرکتوری‌های خروجی در صورت عدم وجود
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# پردازش هر فرد
for person_name in os.listdir(source_dir):
    person_path = os.path.join(source_dir, person_name)

    # بررسی اینکه مسیر یک پوشه است
    if os.path.isdir(person_path):
        json_files = [f for f in os.listdir(person_path) if f.endswith(".json")]
        
        # اگر تعداد فایل‌ها کم است، از آن عبور کن
        if len(json_files) < 2:
            continue
        
        # شافل کردن فایل‌ها برای انتخاب تصادفی
        random.shuffle(json_files)

        # محاسبه تعداد فایل‌های ترین و تست
        split_index = int(len(json_files) * 0.8)
        train_files = json_files[:split_index]
        test_files = json_files[split_index:]

        # مسیرهای خروجی برای این فرد
        person_train_dir = os.path.join(train_dir, person_name)
        person_test_dir = os.path.join(test_dir, person_name)

        os.makedirs(person_train_dir, exist_ok=True)
        os.makedirs(person_test_dir, exist_ok=True)

        # کپی فایل‌ها به دایرکتوری‌های مربوطه
        for file in train_files:
            shutil.copy(os.path.join(person_path, file), os.path.join(person_train_dir, file))

        for file in test_files:
            shutil.copy(os.path.join(person_path, file), os.path.join(person_test_dir, file))

print("تقسیم‌بندی داده‌ها به دایرکتوری‌های Train و Test انجام شد.")
