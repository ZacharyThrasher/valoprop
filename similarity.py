from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def cosine_similarity_model(array1, array2):
    # Convert the arrays to numpy arrays
    array1 = np.array(array1)
    array2 = np.array(array2)

    # Reshape the arrays to be 2-dimensional
    array1 = array1.reshape(1, -1)
    array2 = array2.reshape(1, -1)

    # Compute the cosine similarity between the arrays
    similarity = cosine_similarity(array1, array2)

    return similarity[0][0]

# Example usage
array1 = [1, 2, 3]
array2 = [4, 5, 6]
similarity_score = cosine_similarity_model(array1, array2)
print(similarity_score)


