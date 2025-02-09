import pandas as pd
import shutil
import os

# مسیر فایل people.csv
people_file = r"C:\Users\mmras\OneDrive\Desktop\archive\New folder\people.csv"
# مسیر اصلی تصاویر
source_dir = r"C:\Users\mmras\OneDrive\Desktop\archive\images/"
# مسیر مقصد برای کپی تصاویر
destination_dir = r"C:\Users\mmras\OneDrive\Desktop\facial regognation Elastic\people_10_images"

# خواندن داده‌های فایل people.csv
people_df = pd.read_csv(people_file)

# فیلتر کردن افرادی که بیش از 10 تصویر دارند
people_with_more_than_10_images = people_df[people_df['images'] > 10]

# بررسی اینکه مقصد وجود داشته باشد یا خیر
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# برای هر فرد، پوشه آن‌ها را کپی می‌کنیم
for _, row in people_with_more_than_10_images.iterrows():
    name = row['name']
    
    # مسیر پوشه فرد در دایرکتوری اصلی
    source_person_folder = os.path.join(source_dir, name)
    
    # مسیر مقصد برای هر فرد
    destination_person_folder = os.path.join(destination_dir, name)
    
    # اطمینان از وجود پوشه مقصد
    if not os.path.exists(destination_person_folder):
        os.makedirs(destination_person_folder)
    
    # کپی تصاویر تا ۱۰ تصویر
    images_to_copy = os.listdir(source_person_folder)

    for img in images_to_copy:
        src_image_path = os.path.join(source_person_folder, img)
        dest_image_path = os.path.join(destination_person_folder, img)
        
        # کپی تصویر
        shutil.copy(src_image_path, dest_image_path)

print("کپی تصاویر با موفقیت انجام شد.")
