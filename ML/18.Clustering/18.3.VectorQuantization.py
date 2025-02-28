# !/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def restore_image(cb, cluster, shape):
    row, col, dummy = shape
    image = np.empty((row, col, 3))
    index = 0
    for r in range(row):
        for c in range(col):
            image[r, c] = cb[cluster[index]]
            index += 1
    return image


def show_scatter(a):
    N = 10
    print('原始数据：\n', a)
    density, edges = np.histogramdd(a, bins=[N,N,N], range=[(0,1), (0,1), (0,1)])
    density /= density.sum()
    x = y = z = np.arange(N)
    d = np.meshgrid(x, y, z)

    fig = plt.figure(1, facecolor='w')
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(d[1], d[0], d[2], c='r', s=100*density/density.max(), marker='o', depthshade=True)
    ax.set_xlabel('红色分量')
    ax.set_ylabel('绿色分量')
    ax.set_zlabel('蓝色分量')
    plt.title('图像颜色三维频数分布', fontsize=13)

    plt.figure(2, facecolor='w')
    den = density[density > 0]
    print(den.shape)
    den = np.sort(den)[::-1]
    t = np.arange(len(den))
    plt.plot(t, den, 'r-', t, den, 'go', lw=2)
    plt.title('图像颜色频数分布', fontsize=13)
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    num_vq = 50
    im = Image.open('.\\lena.png')     # son.bmp(100)/flower2.png(200)/son.png(60)/lena.png(50)
    image = np.array(im).astype(np.float) / 255
    image = image[:, :, :3]
    image_v = image.reshape((-1, 3))
    show_scatter(image_v)

    N = image_v.shape[0]    # 图像像素总数
    # 选择足够多的样本(如1000个)，计算聚类中心
    idx = np.random.randint(0, N, size=1000)
    image_sample = image_v[idx]
    model = KMeans(num_vq)
    model.fit(image_sample)
    c = model.predict(image_v)  # 聚类结果
    print('聚类结果：\n', c)
    print('聚类中心：\n', model.cluster_centers_)

    plt.figure(figsize=(12, 6), facecolor='w')
    plt.subplot(121)
    plt.axis('off')
    plt.title('原始图片', fontsize=14)
    plt.imshow(image)
    # plt.savefig('1.png')

    plt.subplot(122)
    vq_image = restore_image(model.cluster_centers_, c, image.shape)
    plt.axis('off')
    plt.title('矢量量化后图片：%d色' % num_vq, fontsize=14)
    plt.imshow(vq_image)
    # plt.savefig('2.png')

    plt.tight_layout(2)
    plt.show()
