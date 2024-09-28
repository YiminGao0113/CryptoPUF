import numpy as np
from sklearn.linear_model import LinearRegression
from tinyjambu import encrypt  # Assuming 'encrypt' is the function from TinyJAMBU

class SimpleTinyJAMBU:
    def __init__(self, key, nonce):
        self.key = key
        self.nonce = nonce

    def encrypt(self, plaintext):
        # Encrypt using TinyJAMBU
        ciphertext = encrypt(plaintext, self.key, self.nonce)
        return ciphertext

# Step 1: Generate TinyJAMBU-based "CRPs" (Challenge-Response Pairs)
num_challenges = 50000  # Number of CRPs to generate
num_bits = 128          # Number of bits in each challenge (to match block size)

# Initialize the SimpleTinyJAMBU with a random key and nonce (128-bit and 96-bit respectively for this example)


# tinyjambu_key = "000102030405060708090A0B0C0D0E0F"  # 16 bytes = 128 bits
# Generate a random 16-byte (128-bit) key
tinyjambu_key = np.random.bytes(16).hex()  # Randomly generated 128-bit key

tinyjambu_nonce = "000000000000000000000000"  # 12 bytes = 96 bits
tinyjambu_cipher = SimpleTinyJAMBU(key=tinyjambu_key, nonce=tinyjambu_nonce)

# Generate challenges (128-bit each)
challenges = np.random.randint(0, 2, size=(num_challenges, num_bits), dtype=np.uint8)

# Encrypt each challenge using TinyJAMBU and treat the encrypted output as the "response"
responses = []
for idx, challenge in enumerate(challenges):
    # Convert the binary challenge to bytes
    challenge_bytes = np.packbits(challenge).tobytes()
    
    # Encrypt the challenge using TinyJAMBU
    encrypted_output = tinyjambu_cipher.encrypt(challenge_bytes)
    
    # Convert the encrypted output back to a binary array
    encrypted_response = np.unpackbits(np.frombuffer(encrypted_output, dtype=np.uint8))
    
    # Use the first bit of the encrypted output as the response (for binary classification)
    responses.append(encrypted_response[65])

responses = np.array(responses)

# Step 2: Prepare data for Linear Regression
X = challenges
y = responses

# Step 3: Train a Linear Regression model
linear_model = LinearRegression()
linear_model.fit(X, y)

# Step 4: Test the model
num_test_challenges = 1000
test_challenges = np.random.randint(0, 2, size=(num_test_challenges, num_bits), dtype=np.uint8)

# Encrypt the test challenges using the same TinyJAMBU key
test_responses = []
for test_challenge in test_challenges:
    test_challenge_bytes = np.packbits(test_challenge).tobytes()
    encrypted_test_output = tinyjambu_cipher.encrypt(test_challenge_bytes)

    encrypted_test_response = np.unpackbits(np.frombuffer(encrypted_test_output, dtype=np.uint8))
    test_responses.append(encrypted_test_response[65])

test_responses = np.array(test_responses)

# Predict responses using the trained Linear Regression model
predicted_responses = linear_model.predict(test_challenges)
predicted_responses = np.round(predicted_responses).astype(int)  # Round to nearest integer for classification

# Print expected vs predicted responses for each test challenge
for i in range(num_test_challenges):
    print(f"Challenge {i+1}:")
    print(f"Expected Response: {test_responses[i]}")
    print(f"Predicted Response: {predicted_responses[i]}")
    print()

# Calculate accuracy
# Calculate bit-level accuracy
total_bits = test_responses.size
correct_bits = np.sum(predicted_responses == test_responses)

bit_accuracy = correct_bits / total_bits
print(f"Bit-level accuracy: {bit_accuracy:.4f}")

# Calculate full-response accuracy (all bits in a challenge must match)
full_response_accuracy = np.mean([np.array_equal(predicted_responses[i], test_responses[i]) for i in range(num_test_challenges)])
print(f"Full-response accuracy: {full_response_accuracy:.4f}")
