import numpy as np
from scipy import misc, ndimage
from sklearn.cluster import KMeans

def colorCluster(colorImage, nColorClusters, showSegmentation = False):
    # Compute the pix image shape
    imageShape = colorImage.shape[0:2]

    # Unroll the image into RGB vector (3 x pix count)
    rgbs = colorImage.reshape((-1, 3)).astype(np.float64)

    # Fit it with a kmeans estimator
    kme = KMeans(init='k-means++', n_clusters=nColorClusters, n_init=10)
    kme.fit(rgbs)

    # Calculate how many points in the image are the clossest to the center
    result = kme.predict(rgbs).reshape(imageShape)

    projected = empty_like(colorImage)
    for i, c in enumerate("RGB"):
        projected[:,:,i] = kme.cluster_centers_[:, i].take(result)
    frequency = [projected.shape[0]*projected.shape[1] - count_nonzero(sum(projected - rgb.astype(int), axis=-1)) for rgb in kme.cluster_centers_]

    # Show the quantized image if desired
    if showSegmentation:
        import pylab as pl
        pl.figure()
        pl.imshow(colorImage)

        pl.figure()
        pl.imshow(projected)
        pl.show()

    # What a derpy attr name. . .
    return kme.cluster_centers_, frequency

if __name__ == "__main__":
    cdata = ndimage.imread("color-wheel-300.png", mode="RGB")
    colorCluster(cdata, 4, showSegmentation=True)
    colorCluster(cdata, 7, showSegmentation=True)
