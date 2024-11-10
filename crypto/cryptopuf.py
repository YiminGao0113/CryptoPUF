import numpy as np
# from tinyjambu import encrypt, SimpleTinyJAMBU
from .tinyjambu.tinyjambu import encrypt, SimpleTinyJAMBU
# from tinyjambu.SimpleTinyJAMBU import SimpleTinyJAMBU
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pypuf.pypuf.simulation import Simulation  # Base class for PUF simulation

class CryptoPUF_TinyJAMBU(Simulation):
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