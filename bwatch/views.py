from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from ultralytics import YOLO
import cv2
import os
from pathlib import Path
import uuid

model = YOLO('BorderWatch/yolov8s.pt')

def detect_objects(request):
    print("Request received: ", request)
    print("Start processing the request.....................................................................................")

    if request.method == 'POST' and request.FILES.get('image'):
        print('Image upload initiated.......................................................................................')
        
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

        # Lire l'image avec OpenCV pour annoter les résultats
        image_cv = cv2.imread(img_path)

        # Dessiner les boîtes et les labels sur l'image
        for r in results:
            for box in r.boxes:
                # Obtenir la classe prédite et les coordonnées de la boîte
                classe = int(box.cls[0])  # Classe prédite (label)
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordonnées de la boîte englobante

                # Dessiner la boîte
                cv2.rectangle(image_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Ajouter le label de l'objet détecté
                label = model.names[classe]
                cv2.putText(image_cv, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Sauvegarder l'image annotée dans un répertoire spécifique
        annotated_filename = f'annotated_{uuid.uuid4()}.jpg'
        annotated_image_path = os.path.join(settings.MEDIA_ROOT, 'detections', annotated_filename)
        cv2.imwrite(annotated_image_path, image_cv)
        print(f'Annotated image saved in: {annotated_image_path}')

        # Créer les chemins vers les images (originale et annotée)
        detection_img_path = os.path.join(settings.MEDIA_URL, 'detections', annotated_filename)
        print(f'Detection image path: {detection_img_path}')

        context = {
            'file_url': file_url,  # Image originale
            'detection_img': detection_img_path  # Image avec objets détectés
        }

        print('Rendering the result template.................................................................................................')
        return render(request, 'bwatch/result.html', context)
    
    print('No image uploaded or incorrect request method..........................................................................................')
    return render(request, 'bwatch/upload.html')

"""def upload_image(request):
    return render(request, 'bwatch/upload.html')"""