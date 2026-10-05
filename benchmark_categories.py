import os
from Backend.ai_verifier import check_consistency

test_dir = r"C:\Users\admin\Downloads\test_category_images"
tests = [
    ("Fruit - True", "apple.jpg", "this is a fresh red apple"),
    ("Fruit - Fake", "apple.jpg", "this image shows a ripe banana fruit"),
    ("Animal - True", "cat.jpg", "this is a cute domestic cat"),
    ("Animal - Fake", "cat.jpg", "this image shows a barking dog"),
    ("Food - True", "pizza.jpg", "this is a delicious margherita pizza"),
    ("Food - Fake", "pizza.jpg", "this image shows a chicken burger"),
    ("Building - True", "eiffel.jpg", "this is the Eiffel Tower in Paris France"),
    ("Building - Fake", "eiffel.jpg", "this is the Taj Mahal monument in India"),
    ("Bike - True", "motorcycle.jpg", "this is a modern motorcycle motorbike"),
    ("Bike - Fake", "motorcycle.jpg", "this is a four wheel electric car"),
    ("Object - True", "laptop.jpg", "this is an open laptop computer on a desk"),
    ("Object - Fake", "laptop.jpg", "this is an electric kitchen blender")
]

print(f"{'Category & Claim':<20} | {'Result':<22} | {'Visual Match':<12} | {'Contradiction':<14}")
print("-" * 75)
for label, fname, claim in tests:
    path = os.path.join(test_dir, fname)
    res = check_consistency(claim, path)
    print(f"{label:<20} | {res['result']:<22} | {res['score']:<12.2f} | {res['contradiction_signal']:<14.2f}")
