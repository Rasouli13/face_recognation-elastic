import os
import cv2
import random
import numpy as np

# مسیر اصلی پوشه افراد
base_dir = r"C:\Users\mmras\OneDrive\Desktop\facial regognation Elastic\people_10_images"

# تعریف توابع افزایش داده
def horizontal_flip(image):
    return cv2.flip(image, 1)

def rotate_image(image):
    angle = random.randint(-30, 30)  # زاویه چرخش بین -30 تا 30
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (w, h))

def adjust_brightness(image):
    factor = random.uniform(0.5, 1.5)  # تغییر روشنایی
    return np.clip(image * factor, 0, 255).astype(np.uint8)

def translate_image(image):
    tx = random.randint(-20, 20)  # ترجمه در محور x
    ty = random.randint(-20, 20)  # ترجمه در محور y
    translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    h, w = image.shape[:2]
    return cv2.warpAffine(image, translation_matrix, (w, h))

def scale_image(image):
    scale_factor = random.uniform(0.8, 1.2)  # تغییر اندازه
    h, w = image.shape[:2]
    new_w, new_h = int(w * scale_factor), int(h * scale_factor)
    return cv2.resize(image, (new_w, new_h))

# لیست متدهای افزایش داده
augmentation_methods = [horizontal_flip, rotate_image, adjust_brightness, translate_image, scale_image]

# برای هر فرد
for person_name in os.listdir(base_dir):
    person_dir = os.path.join(base_dir, person_name)  # مسیر پوشه فرد
    
    if os.path.isdir(person_dir):
        images = os.listdir(person_dir)  # لیست تصاویر موجود
        current_image_count = len(images)  # تعداد تصاویر فعلی
        
        # اگر تعداد تصاویر کمتر از 30 باشد
        while current_image_count < 30:
            # انتخاب یک تصویر به صورت تصادفی
            image_name = random.choice(images)
            image_path = os.path.join(person_dir, image_name)
            
            # خواندن تصویر
            image = cv2.imread(image_path)
            
            # انتخاب تصادفی دو متد افزایش داده
            chosen_methods = random.sample(augmentation_methods, 3)
            
            # اعمال متدهای انتخاب‌شده
            augmented_image = image
            for method in chosen_methods:
                augmented_image = method(augmented_image)
            
            # ذخیره تصویر جدید
            new_image_name = f"{os.path.splitext(image_name)[0]}_aug_{current_image_count}.jpg"
            new_image_path = os.path.join(person_dir, new_image_name)
            cv2.imwrite(new_image_path, augmented_image)
            
            current_image_count += 1

print("افزایش داده‌ها برای هر فرد انجام شد و تعداد تصاویر به 30 رسید.")
