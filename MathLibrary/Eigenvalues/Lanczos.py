import numpy as np

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