MOBILE COMPUTING Q1–Q7: RUNNABLE IMPLEMENTATION PACK

CONTENTS
- Q1_offline_sync.py
- Q2_FDMA_TDMA.py
- Q3_CDMA.py
- Q4_OFDMA.py
- Q5_SDMA.py
- Q6_access_selection.py
- Q7_OFDMA_fairness.py
- Matching .txt output files and *_output_screenshot.png captures

REQUIREMENTS
Python 3.9 or newer
Install required packages once:
    py -m pip install numpy pandas matplotlib pillow

RUN
Open Command Prompt in this folder and run:
    py Q1_offline_sync.py
    py Q2_FDMA_TDMA.py
    py Q3_CDMA.py
    py Q4_OFDMA.py
    py Q5_SDMA.py
    py Q6_access_selection.py
    py Q7_OFDMA_fairness.py

Each program prints its results in the terminal. Q7 also creates CSV result files and graphs in the current folder. The PNG files named *_output_screenshot.png are prepared terminal-output captures for reference.
For submission, it is best to run each script on your own computer and take a fresh screenshot showing:
1. the script filename in the editor, and
2. the complete terminal output after execution.

QUESTION-TO-IMPLEMENTATION MAP
Q1: Offline store-and-forward simulation (Python random)
Q2: FDMA vs TDMA resource/capacity simulation (NumPy)
Q3: DS-CDMA spreading, despreading, BER and code correlation (NumPy)
Q4: OFDMA subcarrier allocation and Jain fairness (NumPy)
Q5: SDMA uniform linear array beam-pattern measurements (NumPy)
Q6: Weighted multiple-access technique decision matrix (NumPy)
Q7: OFDMA maximum-rate vs proportional-fair redesign (NumPy, pandas, Matplotlib)

NOTE
These are reproducible teaching simulations, not commercial radio-network simulators.
The Q5 output reports array-pattern estimates, not full multi-user SINR.
