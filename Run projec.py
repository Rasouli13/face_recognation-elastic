import os
import json
from elasticsearch import Elasticsearch
from sklearn.metrics import classification_report, precision_recall_fscore_support

# اتصال به Elasticsearch
es = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=("elastic", "elastic")  # جایگزین رمز عبور واقعی
)

# مسیر پوشه تست
base_path = r"C:\Users\mmras\OneDrive\Desktop\facial regognation Elastic\people_JSONs_train-test\test"

# متغیرهای جمع‌آوری اطلاعات برای ارزیابی
y_true = []  # نام‌های واقعی
y_pred = []  # نام‌های پیش‌بینی‌شده

# پیمایش پوشه‌ها و فایل‌های JSON
for person_folder in os.listdir(base_path):
    person_path = os.path.join(base_path, person_folder)
    if os.path.isdir(person_path):
        for json_file in os.listdir(person_path):
            if json_file.endswith(".json"):
                file_path = os.path.join(person_path, json_file)
                with open(file_path, "r") as f:
                    data = json.load(f)

                # بررسی وجود فیلدهای موردنیاز
                if "face_name" in data and "face_encoding" in data:
                    true_name = data["face_name"]
                    face_encoding = data["face_encoding"]
                else:
                    print(f"Invalid data in {file_path}")
                    continue

                y_true.append(true_name)

                # ارسال به Elasticsearch
                response = es.search(
                    index="faces",
                    body={
                        "size": 1,
                        "_source": "face_name",
                        "query": {
                            "script_score": {
                                "query": {
                                    "match_all": {}
                                },
                                "script": {
                                    "source": "cosineSimilarity(params.query_vector, 'face_encoding')",
                                    "params": {
                                        "query_vector": face_encoding
                                    }
                                }
                            }
                        }
                    }
                )

                # گرفتن نتیجه از Elasticsearch
                if response["hits"]["hits"] and response["hits"]["hits"][0]["_score"] > 0.93:
                    predicted_name = response["hits"]["hits"][0]["_source"]["face_name"]
                else:
                    predicted_name = "Unknown"

                y_pred.append(predicted_name)
                print(f"True: {true_name}, Predicted: {predicted_name}")

# محاسبه تعداد پیش‌بینی‌ها و پیش‌بینی‌های صحیح
total_predictions = len(y_pred)
correct_predictions = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)

# محاسبه دقت کلی
overall_accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0

# محاسبه Precision, Recall و F1-Score کلی
precision, recall, f1_score, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)

# نمایش گزارش دسته‌بندی
print("\nClassification Report:")
print(classification_report(y_true, y_pred, zero_division=0))

# نمایش نتایج کلی
print("\nOverall Results:")
print(f"Total Predictions: {total_predictions}")
print(f"Correct Predictions: {correct_predictions}")
print(f"Overall Accuracy: {overall_accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1_score:.2f}")
