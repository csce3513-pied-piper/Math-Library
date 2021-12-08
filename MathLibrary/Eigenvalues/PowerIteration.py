import numpy as np

def PowerIteration(A, num_iters = 100):
    # Starting vector
    b = np.random.rand(A.shape[0])

    # Power iteration
    for ii in range(num_iters):
        
        # Project
        bnew = A @ b
        
        # Normalize
        b = bnew / np.linalg.norm(bnew, ord=2)