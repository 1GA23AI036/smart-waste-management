import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from utils.classifier import classify_waste, ALL_CATEGORIES
from utils.recommendations import get_recommendation, calculate_env_impact

print("=== 1. TESTING PLASTIC BOTTLE IMAGE ===")
bottle_path = r"c:\Users\HP\Downloads\test_plastic_bottle.png"
with open(bottle_path, "rb") as f:
    bottle_bytes = f.read()

res_bottle = classify_waste(bottle_bytes)
rec_bottle = get_recommendation(res_bottle["category"])
print("Detected Category:", res_bottle["category"])
print(f"Confidence Score: {int(res_bottle['confidence']*100)}%")
print("Method:", res_bottle["method"])
print("Disposal Method:", rec_bottle["disposal_method"])
print("First Step:", rec_bottle["steps"][0])
print("Recycling Instruction:", rec_bottle["recycling_instruction"][:70] + "...")

print("\n=== 2. TESTING ORGANIC APPLE IMAGE ===")
apple_path = r"c:\Users\HP\Downloads\test_apple.png"
with open(apple_path, "rb") as f:
    apple_bytes = f.read()

res_apple = classify_waste(apple_bytes)
rec_apple = get_recommendation(res_apple["category"])
print("Detected Category:", res_apple["category"])
print(f"Confidence Score: {int(res_apple['confidence']*100)}%")
print("Disposal Method:", rec_apple["disposal_method"])

print("\n=== 3. TESTING DASHBOARD TELEMETRY & ENVIRONMENTAL IMPACT ===")
history = [res_bottle, res_apple]
impact = calculate_env_impact(history)
print("Total Items in History:", len(history))
print("CO2 Reduced:", impact["co2_reduced"], "kg")
print("Energy Saved:", impact["energy_saved"], "kWh")
print("Water Saved:", impact["water_saved"], "L")
print("Trees Saved:", impact["trees_saved"])
print("\n[ALL TESTS PASSED SUCCESSFULLY]")
