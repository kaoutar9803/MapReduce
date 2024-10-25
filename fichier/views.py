from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from hdfs import InsecureClient
import subprocess

# Configuration HDFS
hdfs_client = InsecureClient('http://localhost:9870/', user='kaoutarkouache')

def upload_file(request):
    word_count = None
    error = None

    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']

            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            try:
                hdfs_client.status('/')
                print("Connexion à HDFS réussie.")
            except Exception as e:
                print(f"Erreur de connexion à HDFS : {e}")
                return render(request, 'fichier/upload.html', {'error': "Erreur de connexion à HDFS."})

            try:
                with open(file_path, 'rb') as file_data:
                    hdfs_client.write(f'/input/{filename}', data=file_data, overwrite=True)
                print(f"Fichier {filename} envoyé avec succès vers HDFS.")
            except Exception as e:
                print(f"Erreur lors de l'envoi du fichier vers HDFS: {e}")
                return render(request, 'fichier/upload.html', {'error': str(e)})

            word_count = count_words_in_hadoop(filename)

    return render(request, 'fichier/upload.html', {'word_count': word_count, 'error': error})


def count_words_in_hadoop(filename):
    command = f"hadoop fs -cat /input/{filename} | wc -w"
    try:
        result = subprocess.check_output(command, shell=True)
        return int(result.strip())
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du comptage des mots: {e}")
        return None
