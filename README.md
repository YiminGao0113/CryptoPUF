# CryptoPUF: A Lightweight and ML-Resilient Strong PUF Based on a Weak PUF and Crypto Core

CryptoPUF is a lightweight, machine-learning-resilient Physically Unclonable Function (PUF) implementation designed for secure, efficient authentication/encryption. By combining a weak PUF (DD-PUF) with a cryptographic encryption core (TinyJAMBU), CryptoPUF provides improved resistance against machine learning attacks and is optimized for low-power IoT and edge devices.

## Features
- **Machine Learning Resilience**: Integrates a cryptographic core to reduce vulnerability to ML-based attacks.
- **Lightweight Design**: Combines a weak PUF with TinyJAMBU encryption to offer security in hardware-constrained environments.
- **Configurable Challenge-Response Pairs (CRPs)**: Supports customizable CRP generation and testing.
- **Ease of Integration**: Modular design for use in various secure hardware applications.

## Installation

### Prerequisites
- Python 3.7+
- Required packages: `numpy`, `scikit-learn`, `matplotlib`

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/CryptoPUF_repo.git
   cd CryptoPUF_repo
2. **Run the example Jupyter notebooks**
   Explore the included notebooks to see how to model a CryptoPUF and evaluate its resilience to various ML attacks.
3. **Paper Results**
    The full results for the CryptoPUF paper are available at [CryptoPUF Results Repository](https://github.com/YiminGao0113/CryptoPUF_results).