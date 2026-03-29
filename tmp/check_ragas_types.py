from ragas.metrics.collections import faithfulness, answer_relevancy
print(f"faithfulness type: {type(faithfulness)}")
print(f"answer_relevancy type: {type(answer_relevancy)}")

try:
    f_instance = faithfulness()
    print("faithfulness is a class/callable, called it.")
except Exception as e:
    print(f"Error calling faithfulness: {e}")
