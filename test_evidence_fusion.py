from src.hazards.evidence_fusion import EvidenceFusion


fusion = EvidenceFusion()


# Scenario 1:
# Strong traction event + weak camera evidence
result_1 = fusion.combine(
    vehicle_score=0.80,
    camera_score=0.20,
)

print("Scenario 1:")
print("Combined score:", round(result_1.combined_score, 3))
print("Confidence:", round(result_1.confidence, 3))


# Scenario 2:
# Strong traction event + strong camera evidence
result_2 = fusion.combine(
    vehicle_score=0.80,
    camera_score=0.80,
)

print("\nScenario 2:")
print("Combined score:", round(result_2.combined_score, 3))
print("Confidence:", round(result_2.confidence, 3))


# Scenario 3:
# Weak evidence from both sources
result_3 = fusion.combine(
    vehicle_score=0.10,
    camera_score=0.10,
)

print("\nScenario 3:")
print("Combined score:", round(result_3.combined_score, 3))
print("Confidence:", round(result_3.confidence, 3))