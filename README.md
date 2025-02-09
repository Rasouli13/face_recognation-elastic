order of files:
1. people_10_images.py (choose people with greater than 10 imges)
2. data_augmentation_to_30_photos.py (increase the number of images for people have less than 30 images to 30)
3. images_to_encodingJSON.py (convert ech image to a 128 dims vector with face name in json)
4. make_train-test.py (splits datas 20% for test)
5. .\curl.exe -k -u "elastic:kx-p2DRTGyi-H*+M1dKM" -X PUT "http://localhost:9200/faces" -H "Content-Type: application/json" (make "faces" index)
6. .\curl.exe -k -u "elastic:kx-p2DRTGyi-H*+M1dKM" -X PUT "https://localhost:9200/faces" -H "Content-Type: application/json" --data-binary "@C:\Users\mmras\OneDrive\Desktop\facial regognation Elastic\mapping.json" (make a mapping in faces index)
7. jsonS_uploader.ps1 (upload each json o ftrain data to elastic)
8. Run projec.py (run tests and search in elastics and calculate precision and recall)
