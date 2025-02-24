import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def extract_frames(video_path):
    """Perskaito vaizdo įrašą ir išskiria visus kadrus."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return frames, fps

def compute_blur_metric(frame):
    """Apskaičiuoja kadrų aštrumo lygį naudojant Laplaso operatorių.
       Didelis rezultatas – aštrus kadras, mažas – suliejęs."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def compute_brightness(frame):
    """Apskaičiuoja vidutinį kadrų apšvietimo lygį."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return np.mean(gray)

def mark_frame(frame):
    """Pažymi kadrą raudonu rėmeliu."""
    marked = frame.copy()
    thickness = max(2, frame.shape[0] // 200)  # dinamiškai pritaikomas rėmelio storis
    cv2.rectangle(marked, (0, 0), (marked.shape[1]-1, marked.shape[0]-1), (0, 0, 255), thickness=thickness)
    return marked

def main(video_path, output_video_path):
    # 1. Išskiriame kadrus iš įvesto vaizdo įrašo
    frames, fps = extract_frames(video_path)
    print("Išskirta kadrų:", len(frames))
    
    # 2. Apskaičiuojame kokybės metrikas kiekvienam kadrui
    features = []
    for frame in frames:
        blur = compute_blur_metric(frame)
        brightness = compute_brightness(frame)
        features.append([blur, brightness])
    features = np.array(features)
    
    # 3. Normalizuojame metrikų duomenis
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # 4. Klasterizacija – čia naudojame K-Means su 3 klasteriais (pvz., mažai, vidutiniškai ir labai sugadinti kadrus)
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)
    
    # 5. Identifikuojame klasterį, kurio vidutinis blur rodiklis yra mažiausias (t. y. labiausiai sugadinti kadrų grupė)
    cluster_blur = {}
    for i in range(n_clusters):
        indices = np.where(clusters == i)[0]
        avg_blur = np.mean(features[indices, 0])
        cluster_blur[i] = avg_blur
    most_damaged_cluster = min(cluster_blur, key=cluster_blur.get)
    print("Labiausiai sugadintų kadrų klasteris:", most_damaged_cluster)
    
    # 6. Sukuriame naują vaizdo įrašą, kuriame sugadinti kadrai pažymėti raudonu rėmeliu
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    for i, frame in enumerate(frames):
        if clusters[i] == most_damaged_cluster:
            frame = mark_frame(frame)
        out.write(frame)
    
    out.release()
    print("Analizės rezultatai išsaugoti:", output_video_path)
    
    # 7. Papildomai – pateikiame diagramos pavidalu kadrų blur metrikos pasiskirstymą ir klasterių susiskirstymą
    plt.figure(figsize=(10,6))
    plt.scatter(range(len(features)), features[:, 0], c=clusters, cmap='viridis')
    plt.xlabel("Kadro numeris")
    plt.ylabel("Blur metrika (Laplacian variacija)")
    plt.title("Kadrų aštrumo metrikos ir klasterizacijos rezultatai")
    plt.colorbar(label="Klasteris")
    plt.show()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Vaizdo įrašo kokybės analizė ir klasterizacija")
    parser.add_argument("--video", type=str, required=True, help="Įvesto vaizdo įrašo kelias")
    parser.add_argument("--output", type=str, required=True, help="Išvesto vaizdo įrašo kelias, kuriame pažymėti sugadinti kadrai")
    args = parser.parse_args()
    main(args.video, args.output)
