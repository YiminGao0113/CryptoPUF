import numpy as np

from tinyjambu import encrypt  # Assuming 'encrypt' is the function from TinyJAMBU
from pypuf.pypuf.simulation import Simulation  # Base class for PUF simulation
from pypuf.pypuf import io
from pypuf.pypuf.metrics import uniqueness, uniqueness_data, bias, bias_data

from pypuf.pypuf.io import random_inputs  # Import to generate challenges if needed
from pypuf.pypuf import attack
from pypuf.pypuf import metrics
import matplotlib.pyplot as plt


class SimpleTinyJAMBU:
    def __init__(self, key, nonce):
        self.key = key
        self.nonce = nonce

    def encrypt(self, plaintext):
        # Encrypt using TinyJAMBU
        ciphertext = encrypt(plaintext, self.key, self.nonce)
        return ciphertext


class CryptoPUF(Simulation):
    def __init__(self, challenge_length: int, key: str, nonce: str, seed: int = None):
        self._challenge_length = challenge_length
        self._response_length = 1  # Set response length to 1, as we want only 1-bit responses
        self.tinyjambu_cipher = SimpleTinyJAMBU(key=key, nonce=nonce)

        if seed:
            np.random.seed(seed)

    @property
    def challenge_length(self) -> int:
        return self._challenge_length

    @property
    def response_length(self) -> int:
        return self._response_length

    def eval(self, challenges: np.ndarray) -> np.ndarray:
        """Evaluate the PUF on a list of given challenges."""
        responses = []
        for challenge in challenges:
            # Convert the challenge from {-1, 1} to {0, 1}
            challenge_binary = 0.5 * (challenge + 1)  # -1 -> 0, 1 -> 1

            # Convert the binary challenge to bytes
            challenge_bytes = np.packbits(challenge_binary.astype(np.uint8)).tobytes()

            # Encrypt using TinyJAMBU
            encrypted_output = self.tinyjambu_cipher.encrypt(challenge_bytes)

            # Convert the encrypted output to binary array (128-bit response)
            encrypted_response = np.unpackbits(np.frombuffer(encrypted_output, dtype=np.uint8))

            # Extract the 65th bit (index 64) from the encrypted response
            bit_65 = encrypted_response[127]

            # Map 0 to -1 and keep 1 as 1
            response = -1 if bit_65 == 0 else 1

            # Append the response
            responses.append(response)

        return np.array(responses)

    def r_eval(self, r: int, challenges: np.ndarray) -> np.ndarray:
        """
        Evaluates the CryptoPUF `r` times on the list of challenges and returns an array
        of shape (r, N, 1) of all responses.
        """
        N = challenges.shape[0]
        responses = np.empty(shape=(N, self.response_length, r))
        # Evaluate the PUF r times
        for i in range(r):
            responses[:, :, i] = self.eval(challenges).reshape(N, self.response_length)
        
        return responses



# Create multiple PUF instances for uniqueness evaluation
puf_instances = []
for i in range(5):  # Create 5 PUF instances
    new_key = np.random.bytes(16).hex()  # New random key for each instance
    nonce = "000000000000000000000000"  # 96-bit nonce for TinyJAMBU
    crypto_puf = CryptoPUF(challenge_length=128, key=new_key, nonce=nonce)
    print(f"key is {new_key}")
    puf_instances.append(crypto_puf)

# Step 1: Evaluate uniqueness using the `uniqueness()` function
uniqueness_score = uniqueness(puf_instances, seed=31415, N=1000)
print(f"Uniqueness score of the responses: {uniqueness_score}")

# m = puf_instances[0].response_length
# print(f"Response length is {m}")
# # Generate 1000 random challenges with length equal to the first PUF's challenge length
# challenges = random_inputs(puf_instances[0].challenge_length, 1000, 31415)
# # Initialize an empty array to store responses, shape = (number of PUF instances, number of challenges, response length)
# responses = np.empty(shape=(len(puf_instances), 1000, m))
# # Evaluate and store responses for each PUF instance
# for i, instance in enumerate(puf_instances):
#     responses[i] = instance.eval(challenges).reshape(1000, m)
#     # Print the last 5 responses for the current PUF instance
#     print(f"Last 5 responses for PUF {i+1}: {responses[i][-5:]}")
# # Calculate and print the uniqueness score
# print(f"Uniqueness score is {uniqueness_data(responses)}")


# Step 2: bias evaluation

# -----------------bias
# Step 2: Evaluate the bias for the first PUF instance
# bias_score = bias(puf_instances[0], seed=31415)
# print(f"bias is {bias_score}")


# puf = puf_instances[0]
# crps = io.ChallengeResponseSet.from_simulation(puf, N=50000, seed=2)
# -------------- Logistic Regression

# Create a Challenge-Response set with the correct number of challenges and responses



# attack = attack.LRAttack2021(crps, seed=3, k=4, bs=1000, lr=.001, epochs=100)
# attack.fit()  
# model = attack.model
# score = metrics.similarity(puf, model, seed=4)
# print(f"score is {score}")


# -------------- MLP
# attack = attack.MLPAttack2021(
#     crps, seed=3, net=[2 ** 4, 2 ** 5, 2 ** 4],
#     epochs=30, lr=.001, bs=1000, early_stop=.08
# )
# attack.fit()  
# model = attack.model
# score = metrics.similarity(puf, model, seed=4)
# print(f"score is {score}")

# Evaluate and train the model with varying CRP sizes
crp_values = np.array([50000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000])
accuracy_scores = []

for N in crp_values:
    print(f"Training with {N} CRPs...")

    # Generate CRPs for the current iteration
    crps = io.ChallengeResponseSet.from_simulation(puf_instances[0], N=N, seed=2)

    # Create and train the LRAttack2021 attack with the generated CRPs
    attack_instance = attack.LRAttack2021(crps, seed=3, k=4, bs=1000, lr=.001, epochs=100)
    attack_instance.fit()

    # Evaluate the model's similarity score
    model = attack_instance.model
    score = metrics.similarity(puf_instances[0], model, seed=4)
    print(f"Accuracy (similarity score) with {N} CRPs: {score}")

    # Store the accuracy score
    accuracy_scores.append(score)

# Plot the accuracy scores against the CRP sizes
plt.figure(figsize=(8, 6))
plt.plot(crp_values / 1000, accuracy_scores, marker='o', linestyle='-', color='b')
plt.xlabel('Number of CRPs (x 10^3)')
plt.ylabel('Accuracy (Similarity Score)')
plt.title('Accuracy vs Number of CRPs for CryptoPUF')
plt.grid(True)
plt.show()

# Print the final accuracy scores for each CRP size
print("Accuracy scores for different CRP sizes:")
for N, score in zip(crp_values, accuracy_scores):
    print(f"{N} CRPs: {score}")

# lr: 
# 5000 CRPs: [0.497]
# 10000 CRPs: [0.491]
# 15000 CRPs: [0.49]
# 20000 CRPs: [0.504]
# 25000 CRPs: [0.464]
# 30000 CRPs: [0.52]
# 35000 CRPs: [0.486]
# 40000 CRPs: [0.503]
# 45000 CRPs: [0.527]
# 50000 CRPs: [0.521]
# +++++++++++++++++
# 150000 CRPs: [0.509]
# 200000 CRPs: [0.504]
# 250000 CRPs: [0.482]
# 300000 CRPs: [0.496]
# 350000 CRPs: [0.515]
# 400000 CRPs: [0.48]
# 450000 CRPs: [0.518]
# 500000 CRPs: [0.502]