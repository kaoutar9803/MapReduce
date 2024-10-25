
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from hdfs import InsecureClient
import subprocess
def upload_file(request):
    word_count = None
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        with open(file_path, 'r') as f:
            text = f.read()
            word_count = len(text.split())

    return render(request, 'fichier/upload.html', {'word_count': word_count})



hdfs_client = InsecureClient('http://localhost:9864/', user='kaoutarkouache')
def upload_file(request):
    word_count = None
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            try:
                hdfs_client.upload('/input', file_path)
            except Exception as e:
                print(f"Erreur lors de l'envoi du fichier vers HDFS: {e}")

            word_count = count_words_in_hadoop(uploaded_file.name)

    return render(request, 'fichier/upload.html', {'word_count': word_count})

def count_words_in_hadoop(filename):
    command = f"hadoop fs -cat /input/{filename} | wc -w"
    try:
        result = subprocess.check_output(command, shell=True)
        return int(result.strip())
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du comptage des mots: {e}")
        return None
