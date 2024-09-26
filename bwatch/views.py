from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from ultralytics import YOLO  
from pathlib import Path

# Charger votre modèle YOLOv8 depuis le fichier .pt
model = YOLO('BorderWatch/yolov8s.pt')

def detect_objects(request):
    print("Request received: ", request)
    print("Start processing the request...")

    if request.method == 'POST' and request.FILES.get('image'):
        print('Image upload initiated...')
        
        # Récupérer l'image uploadée
        image = request.FILES['image']
        print(f'Uploaded image name: {image.name}')
        
        # Sauvegarder l'image temporairement
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_url = fs.url(filename)
        print(f'Temporary image saved at: {filename}')

        # Effectuer la détection
        img_path = fs.path(filename)
        print(f'Performing detection on image: {img_path}')
        results = model(img_path)
        print(results)

        # Sauvegarder l'image annotée
        detection_path = Path('media/detections') / Path(filename).name 
        results.save() 

        print(f'Annotated image saved in: {detection_path}')

        # Créer le chemin vers l'image avec objets détectés
        detection_img_path = detection_path.as_posix()
        print(f'Detection image path: {detection_img_path}')

        context = {
            'file_url': file_url,  # Image originale
            'detection_img': detection_img_path  # Image avec objets détectés
        }
        
        print('Rendering the result template...')
        return render(request, 'bwatch/result.html', context)
    
    print('No image uploaded or incorrect request method.')
    return render(request, 'bwatch/upload.html')
