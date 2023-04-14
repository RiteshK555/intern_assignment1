# from django.conf import settings
# import os
# from django.http import FileResponse

# def convert_rb_format(file_name):
#     index = file_name.find("/images")
#     if index != -1:
#         file_name = file_name[index:]
#     else:
#         print("wrong url")
#     file_path = os.path.join(settings.BASE_DIR , file_name)
#     print(settings.MEDIA_ROOT)
#     print(settings.BASE_DIR)
#     print(file_path)
#     # print(file_path + "################################################")
#     file_ext = os.path.splitext(file_path)[1]
#     content_type = None
#     with open(file_path, 'rb') as f:
#         image_data = f.read()
#     if file_ext == '.jpg' or file_ext == '.jpeg':
#         content_type = 'image/jpeg'
#     elif file_ext == '.png':
#         content_type = 'image/png'
#     res = FileResponse(image_data, content_type = content_type)
#     return res