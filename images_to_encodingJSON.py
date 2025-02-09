import os
import face_recognition
import json

# مسیر اصلی پوشه افراد
base_dir = r"C:\Users\mmras\OneDrive\Desktop\facial regognation Elastic\people_10_images"
# مسیر دایرکتوری مقصد برای ذخیره فایل‌های JSON
output_dir = r"C:\Users\mmras\OneDrive\Desktop\facial regognation Elastic\people_JSONs"
# ایجاد دایرکتوری مقصد اگر وجود ندارد
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# پردازش پوشه هر فرد
for person_name in os.listdir(base_dir):
    person_dir = os.path.join(base_dir, person_name)  # مسیر پوشه فرد

    # بررسی اینکه مسیر یک پوشه است
    if os.path.isdir(person_dir):
        print(f"در حال پردازش پوشه فرد: {person_name}")

        # ایجاد دایرکتوری مخصوص فرد در پوشه مقصد
        person_output_dir = os.path.join(output_dir, person_name)
        if not os.path.exists(person_output_dir):
            os.makedirs(person_output_dir)
        
        # پردازش تصاویر در پوشه فرد
        images = os.listdir(person_dir)
        for i, image_name in enumerate(images):
            print(f"در حال پردازش تصویر {image_name} از پوشه {person_name}")

            image_path = os.path.join(person_dir, image_name)  # مسیر تصویر

            try:
                # بارگذاری تصویر
                image = face_recognition.load_image_file(image_path)

                # شناسایی مکان‌های چهره‌ها
                face_locations = face_recognition.face_locations(image)

                # استخراج انکدینگ چهره
                face_encodings = face_recognition.face_encodings(image, face_locations)

                # ایجاد فایل JSON برای هر چهره شناسایی‌شده
                for j, face_encoding in enumerate(face_encodings):
                    json_data = {
                        "face_name": person_name,
                        "face_encoding": face_encoding.tolist()
                    }

                    # نام فایل JSON
                    json_file_name = f"{i + 1:04d}.json"  # نام فایل به صورت 0001، 0002، ...
                    json_file_path = os.path.join(person_output_dir, json_file_name)

                    # ذخیره فایل JSON
                    with open(json_file_path, "w") as json_file:
                        json.dump(json_data, json_file, indent=4)

            except Exception as e:
                print(f"خطا در پردازش تصویر {image_name}: {e}")

print("تمام فایل‌های JSON تولید شدند.")
