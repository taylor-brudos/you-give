import os
def handle_uploaded_file(file,filename):
    if not os.path.exists('./apps/first_app/static/first_app/upload'):
        os.mkdir('./apps/first_app/static/first_app/upload/')
    # print(filename)
 
    with open('./apps/first_app/static/first_app/upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)