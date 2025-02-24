import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from brisque import BRISQUE
import argparse

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
       Mažesnė vertė – labiau suliejęs (blogesnės kokybės) kadras."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def compute_brightness(frame):
    """Apskaičiuoja vidutinį kadrų apšvietimo lygį."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return np.mean(gray)

def compute_brisque_score(frame, brisque_obj):
    """Apskaičiuoja BRISQUE kokybės balą naudojant pybrisque biblioteką.
       Aukštesnis balas rodo blogesnę vaizdo kokybę."""
    # Jei reikia, galima konvertuoti į tinkamą spalvų erdvę (pvz., RGB), priklausomai nuo bibliotekos reikalavimų.
    score = brisque_obj.score(frame)
    return score

def mark_frame(frame):
    """Pažymi kadrą raudonu rėmeliu."""
    marked = frame.copy()
    thickness = max(2, frame.shape[0] // 200)  # Dinamiškai pritaikomas rėmelio storis
    cv2.rectangle(marked, (0, 0), (marked.shape[1]-1, marked.shape[0]-1), (0, 0, 255), thickness=thickness)
    return marked

def main(video_path, output_video_path):
    # 1. Išskiriame kadrus iš įvesto vaizdo įrašo
    frames, fps = extract_frames(video_path)
    print("Išskirta kadrų:", len(frames))
    
    # Inicializuojame BRISQUE objektą
    brisque_obj = BRISQUE()
    
    # 2. Apskaičiuojame metrikas kiekvienam kadro: blur, brightness ir BRISQUE balą
    features = []
    for frame in frames:
        blur = compute_blur_metric(frame)
        brightness = compute_brightness(frame)
        brisque_score = compute_brisque_score(frame, brisque_obj)
        features.append([blur, brightness, brisque_score])
    features = np.array(features)
    
    # 3. Normalizuojame duomenis
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # 4. Klasterizacija – naudojame K-Means su 3 klasteriais
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)
    
    # 5. Pasirenkame klasterį, kurio vidutinis BRISQUE balas yra aukščiausias (blogiausia kokybė)
    cluster_brisque = {}
    for i in range(n_clusters):
        indices = np.where(clusters == i)[0]
        avg_brisque = np.mean(features[indices, 2])
        cluster_brisque[i] = avg_brisque
    worst_cluster = max(cluster_brisque, key=cluster_brisque.get)
    print("Labiausiai sugadintų kadrų klasteris:", worst_cluster)
    
    # 6. Sukuriame naują vaizdo įrašą, kuriame sugadinti kadrai pažymėti raudonu rėmeliu
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    for i, frame in enumerate(frames):
        if clusters[i] == worst_cluster:
            frame = mark_frame(frame)
        out.write(frame)
    
    out.release()
    print("Analizės rezultatai išsaugoti:", output_video_path)
    
    # 7. Parodome diagramos pavidalu kadrų blur metrikos pasiskirstymą bei klasterių susiskirstymą
    plt.figure(figsize=(10,6))
    plt.scatter(range(len(features)), features[:, 0], c=clusters, cmap='viridis')
    plt.xlabel("Kadro numeris")
    plt.ylabel("Blur metrika (Laplacian variacija)")
    plt.title("Kadrų aštrumo metrikos ir klasterizacijos rezultatai")
    plt.colorbar(label="Klasteris")
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Vaizdo įrašo kokybės analizė ir klasterizacija su BRISQUE")
    parser.add_argument("--video", type=str, required=True, help="Įvesto vaizdo įrašo kelias")
    parser.add_argument("--output", type=str, required=True, help="Išvesto vaizdo įrašo kelias, kuriame pažymėti sugadinti kadrai")
    args = parser.parse_args()
    main(args.video, args.output)
