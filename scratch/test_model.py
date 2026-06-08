from transformers import pipeline

try:
    print("Loading model...")
    pipe = pipeline("text-classification", model="sentinet/suicidality")
    print("Model loaded. Testing classification...")
    res = pipe("I want to kill myself")
    print("Result 1:", res)
    res2 = pipe("Hello, how are you?")
    print("Result 2:", res2)
except Exception as e:
    print("Error:", e)
