import numpy as np
from collections import Counter

def load_train(path):
    """Carga datos de entrenamiento con etiquetas de clase al final."""
    X_list, y_list = [], []
    with open(path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(',')
            feats = list(map(float, parts[:4]))
            label = parts[4]
            X_list.append(feats)
            y_list.append(label)
    X = np.array(X_list)
    label_map = {"Iris-setosa": 0, "Iris-versicolor": 1}
    y = np.array([label_map[l] for l in y_list])
    return X, y

def load_test(path):
    """Carga datos de test, descarta columna de etiqueta si existe."""
    X_list = []
    with open(path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(',')
            feats = list(map(float, parts[:4]))
            X_list.append(feats)
    return np.array(X_list)

def fuzzy_kmeans(X, k, tol=0.01, b=2, max_iter=100):
    centroids = np.array([[4.6,3.0,4.0,0.0],[6.8,3.4,4.6,0.7]])
    for _ in range(max_iter):
        dist = np.linalg.norm(X[:,None]-centroids[None,:],axis=2)
        dist = np.maximum(dist,1e-6)
        U = (1.0/dist**(2/(b-1)))
        U /= U.sum(axis=1,keepdims=True)
        new_cent = np.zeros_like(centroids)
        for i in range(k):
            w = U[:,i]**b
            new_cent[i] = (w[:,None]*X).sum(axis=0)/w.sum()
        if np.max(np.linalg.norm(new_cent-centroids,axis=1))<tol: break
        centroids = new_cent
    return centroids

def bayes_train(X, y):
    params={}
    for c in np.unique(y):
        Xc=X[y==c]
        params[c]=(Xc.mean(axis=0), np.cov(Xc,rowvar=False), Xc.shape[0]/X.shape[0])
    return params

def bayes_predict(X, params):
    preds=[]
    for x in X:
        scores={}
        for c,(mu,C,prior) in params.items():
            d=x-mu; det=np.linalg.det(C); inv=np.linalg.inv(C)
            coef=1/((2*np.pi)**(len(x)/2)*np.sqrt(det))
            like=coef*np.exp(-0.5*d.dot(inv).dot(d))
            scores[c]=like*prior
        preds.append(max(scores,key=scores.get))
    return np.array(preds)

def lloyd(X, k, eta=0.1, max_iter=10):
    centroids = np.array([[4.6,3.0,4.0,0.0],[6.8,3.4,4.6,0.7]])
    for _ in range(max_iter):
        for x in X:
            j=np.argmin(np.linalg.norm(centroids-x,axis=1))
            centroids[j]+=eta*(x-centroids[j])
    return centroids

def map_clusters(X,y,centroids):
    labels=np.argmin(np.linalg.norm(X[:,None]-centroids[None,:],axis=2),axis=1)
    m={}
    for cl in np.unique(labels): m[cl]=Counter(y[labels==cl]).most_common(1)[0][0]
    return m

def cluster_predict(X,centroids,mapping):
    labels=np.argmin(np.linalg.norm(X[:,None]-centroids[None,:],axis=2),axis=1)
    return np.array([mapping[l] for l in labels])

if __name__=='__main__':
    # Datos y tests
    X_train,y_train=load_train('Iris2Clases.txt')
    tests=['TestIris01.txt','TestIris02.txt','TestIris03.txt']
    inv={0:'Iris-setosa',1:'Iris-versicolor'}

    # Calcular resultados
    res = {}
    # K-Means Borroso
    c1 = fuzzy_kmeans(X_train, 2)
    m1 = map_clusters(X_train, y_train, c1)
    res['Fuzzy K-Means'] = [', '.join(inv[p] for p in cluster_predict(load_test(f), c1, m1)) for f in tests]

    # Bayes
    params = bayes_train(X_train, y_train)
    # Extraer matrices de covarianza para mostrar
    covs = {inv[c]: params[c][1] for c in params}
    res['Bayes'] = [', '.join(inv[p] for p in bayes_predict(load_test(f), params)) for f in tests]

    # Lloyd
    c3 = lloyd(X_train, 2)
    m3 = map_clusters(X_train, y_train, c3)
    res['Lloyd'] = [', '.join(inv[p] for p in cluster_predict(load_test(f), c3, m3)) for f in tests]

# Interfaz con tkinter y ttk.Notebook
try:
    import tkinter as tk
    from tkinter import ttk
    root = tk.Tk()
    root.title('Resultados de Clasificación')
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill='both', padx=10, pady=10)
    for method, outs in res.items():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=method)
        # Mostrar medias
        ttk.Label(frame, text='Medias/inciales:', font=('Arial', 10, 'bold'), padding=(10,5)).pack(anchor='w')
        if method == 'Bayes':
            for c, (mu, _, _) in params.items():
                cls_name = inv[c]
                ttk.Label(frame, text=f"{cls_name}: {np.array2string(mu, precision=2, suppress_small=True)}", padding=(20,5)).pack(anchor='w')
        else:
            cents = c1 if method == 'Fuzzy K-Means' else c3
            for idx, cent in enumerate(cents):
                ttk.Label(frame, text=f"Centro {idx+1}: {np.array2string(cent, precision=2, suppress_small=True)}", padding=(20,5)).pack(anchor='w')
        # Espacio tras medias
        ttk.Label(frame, text='').pack()
        # Mostrar contenido según método
        if method == 'Bayes':
            ttk.Label(frame, text='Matrices de covarianza:', font=('Arial', 10, 'bold'), padding=(10,5)).pack(anchor='w')
            ttk.Label(frame, text='').pack()
            for cls, C in covs.items():
                ttk.Label(frame, text=f"{cls}: {np.array2string(C, precision=2, suppress_small=True)}", padding=(20,5)).pack(anchor='w')
            ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=5)
        for fname, res_str in zip(tests, outs):
            lbl = ttk.Label(frame, text=f"{fname}: {res_str}", padding=(10,5))
            lbl.pack(anchor='w')
    root.mainloop()
except Exception as e:
    print('Error GUI, mostrando consola:', e)
    for method, outs in res.items():
        print(f'--- {method} ---')
        for fname, out in zip(tests, outs): print(f"{fname}: {out}")
