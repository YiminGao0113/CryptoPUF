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


# Function to evaluate the average bias over multiple PUF instances
def evaluate_avg_bias(num_puf_instances: int, seed: int):
    bias_scores = []

    for i in range(num_puf_instances):
        # Create a new PUF instance
        new_key = np.random.bytes(16).hex()  # New random key for each instance
        nonce = "000000000000000000000000"  # 96-bit nonce for TinyJAMBU
        crypto_puf = CryptoPUF(challenge_length=128, key=new_key, nonce=nonce)

        # Evaluate bias for the current PUF instance
        bias_score = bias(crypto_puf, seed=seed)
        bias_scores.append(bias_score)

    # Compute the average bias across all instances
    avg_bias = np.mean(bias_scores)

    return avg_bias


# Main script to initialize PUF instances and compute average uniqueness and bias
num_puf_instances = 500  # Number of PUF instances to average
num_challenges = 1000   # Number of challenges for uniqueness
seed = 31415

# Step 1: Create 5 PUF instances for uniqueness evaluation
puf_instances = []
for i in range(5):  # Create 5 PUF instances
    new_key = np.random.bytes(16).hex()  # New random key for each instance
    nonce = "000000000000000000000000"  # 96-bit nonce for TinyJAMBU
    crypto_puf = CryptoPUF(challenge_length=128, key=new_key, nonce=nonce)
    print(f"key is {new_key}")
    puf_instances.append(crypto_puf)

# Step 2: Evaluate uniqueness
uniqueness_score = uniqueness(puf_instances, seed=31415, N=1000)
print(f"Uniqueness score of the responses: {uniqueness_score}")

# Step 3: Evaluate the average bias across 20 PUF instances
avg_bias_score = evaluate_avg_bias(num_puf_instances, seed=31415)
print(f"Average bias across {num_puf_instances} PUF instances: {avg_bias_score}")
