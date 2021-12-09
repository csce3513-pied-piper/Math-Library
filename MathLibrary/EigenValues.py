import numpy as np
from numpy import array, zeros, diag, diagflat, dot

def arnoldi_iteration(A, b, n):
    m = A.shape[0]

    h = np.zeros((n + 1, n), dtype=np.complex)
    Q = np.zeros((m, n + 1), dtype=np.complex)

    q = b / np.linalg.norm(b)
    Q[:, 0] = q

    for k in range(n):
        v = A.dot(q)
        for j in range(k + 1):
            h[j, k] = np.dot(Q[:, j].conj(), v)  # <-- Q needs conjugation!
            v = v - h[j, k] * Q[:, j]

        h[k + 1, k] = np.linalg.norm(v)
        eps = 1e-12
        if h[k + 1, k] > eps:
            q = v / h[k + 1, k]
            Q[:, k + 1] = q
        else:
            return Q, h
    return Q, h

def jacobi(A,b,N=25,x=None):
    """Solves the equation Ax=b via the Jacobi iterative method."""
    # Create an initial guess if needed                                                                                                                                                            
    if x is None:
        x = zeros(len(A[0]))

    # Create a vector of the diagonal elements of A                                                                                                                                                
    # and subtract them from A                                                                                                                                                                     
    D = diag(A)
    R = A - diagflat(D)

    # Iterate for N times                                                                                                                                                                          
    for i in range(N):
        x = (b - dot(R,x)) / D
    return x

def Lanczos( A, v, m=100 ):
    n = len(v)
    if m>n: m = n;
    # from here https://en.wikipedia.org/wiki/Lanczos_algorithm
    V = np.zeros( (m,n) )
    T = np.zeros( (m,m) )
    V[0, :] = v

    # step 2.1 - 2.3 in https://en.wikipedia.org/wiki/Lanczos_algorithm
    w = np.dot(A, v[0,:])
    alfa = np.dot(w,v[0,:])
    w = w - alfa*V[:, 0]
    T[0,0] = alfa

    # needs to start the iterations from indices 1
    for j in range(1, m-1 ):
        beta = np.sqrt( np.dot( w, w ) )

        V[j,:] = w/beta

        # This performs some rediagonalization to make sure all the vectors are orthogonal to eachother
        for i in range(j-1):
            V[j, :] = V[j,:] - np.dot(np.conj(V[j,:]), V[i, :])*V[i,:]
        V[j, :] = V[j, :]/np.linalg.norm(V[j, :])


        w = np.dot(A, V[j, :])
        alfa = np.dot(w, V[j, :])
        w = w - alfa * V[j, :] - beta*V[j-1, :]

        T[j,j  ] = alfa
        T[j-1 ,j] = beta
        T[j,j-1] = beta


    return T, V

def PowerIteration(A, num_iters = 100):
    # Starting vector
    b = np.random.rand(A.shape[0])

    # Power iteration
    for ii in range(num_iters):
        
        # Project
        bnew = A @ b
        
        # Normalize
        b = bnew / np.linalg.norm(bnew, ord=2)
