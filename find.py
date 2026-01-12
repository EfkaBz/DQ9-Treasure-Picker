import os
import cv2
import numpy as np

QUERY_IMG = os.path.join("query", "treasure.png")
LOC_DIR = os.path.join("maps", "localisation_treasure")

THRESHOLD = 0.65          # score minimum pour être "fiable"
DELTA_SECOND = 0.03       # tolérance pour afficher un 2e résultat

def load_gray(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(path)
    return img

def resize_to(img, target):
    return cv2.resize(
        img,
        (target.shape[1], target.shape[0]),
        interpolation=cv2.INTER_AREA
    )

def main():
    if not os.path.exists(QUERY_IMG):
        print("❌ query/treasure.png introuvable")
        return

    query = load_gray(QUERY_IMG)
    results = []

    for fname in sorted(os.listdir(LOC_DIR)):
        if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        path = os.path.join(LOC_DIR, fname)
        loc = load_gray(path)

        loc_resized = resize_to(loc, query)
        score = cv2.matchTemplate(query, loc_resized, cv2.TM_CCOEFF_NORMED)[0][0]
        results.append((score, fname))

    results.sort(reverse=True, key=lambda x: x[0])

    best_score, best_name = results[0]

    print("🎯 Meilleur candidat :")
    print(f"- {best_name} | score={best_score:.3f}")

    # Cas fiable
    if best_score >= THRESHOLD:
        print("\n✅ Correspondance fiable")

        if len(results) > 1:
            second_score, second_name = results[1]
            if abs(best_score - second_score) <= DELTA_SECOND:
                print("\n⚠️ Deux résultats très proches :")
                print(f"- {best_name}   | score={best_score:.3f}")
                print(f"- {second_name} | score={second_score:.3f}")

    # Cas non fiable mais affiché
    else:
        print("\n⚠️ Correspondance NON fiable (score trop bas)")
        if len(results) > 1:
            second_score, second_name = results[1]
            if abs(best_score - second_score) <= DELTA_SECOND:
                print("\n⚠️ Ambiguïté possible :")
                print(f"- {best_name}   | score={best_score:.3f}")
                print(f"- {second_name} | score={second_score:.3f}")

if __name__ == "__main__":
    main()
