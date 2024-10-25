from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import subprocess


def upload_file(request):
    word_count = None

    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']

            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            hdfs_upload_command = f"hadoop fs -put -f {file_path} /input/{filename}"

            try:
                subprocess.check_call(hdfs_upload_command, shell=True)
                print(f"Fichier {filename} envoyé avec succès vers HDFS.")

                word_count = count_words_in_hadoop(filename)

            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'envoi du fichier vers HDFS: {e}")
                return render(request, 'fichier/upload.html', {'word_count': None, 'error': str(e)})

    return render(request, 'fichier/upload.html', {'word_count': word_count})


def count_words_in_hadoop(filename):
    command = f"hadoop fs -cat /input/{filename} | wc -w"
    try:
        result = subprocess.check_output(command, shell=True)
        return int(result.strip())
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du comptage des mots: {e}")
        return None
