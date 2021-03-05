# 数式
> θの求め方
$$
\alpha = 
    \tan^{-1}
    \Bigl(
        \frac{y_a-y_b}{x_a-x_b}
    \Bigr)
$$
> ポール間をx軸としたときの障害物の座標
$$
u = r \cos\theta \\
v = r \sin\theta
$$
> 上記の障害物座標を平面直角座標に変換
$$
\begin{pmatrix}
    X \\
    Y
\end{pmatrix}
=
    \begin{pmatrix}
        \cos\alpha & -\sin\alpha \\
        \sin\alpha & \cos\alpha
    \end{pmatrix}
    \begin{pmatrix}
        u \\
        v
    \end{pmatrix}
    +
    \begin{pmatrix}
        x_a \\
        y_a
    \end{pmatrix}
$$
