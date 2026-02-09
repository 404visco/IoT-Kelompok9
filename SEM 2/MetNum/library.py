def turunan(f, x, h):
    return (f(x + h) - f(x)) / h

def newton_raphson(f, toleransi=1e-4, iterasi_max=100):
    x = f/2
    iterasi = 0

    while iterasi < iterasi_max:
        fx = f(x)
        dfx = turunan(f)

        if dfx == 0:
            raise ValueError("Turunan bernilai nol, Newton–Raphson gagal")

        x_baru = x - fx / dfx

        if abs(x_baru - x) <= toleransi:
            return x_baru

        x = x_baru
        iterasi += 1

    return x

# def f(x):
#     return x  # x^2 - 2

# def df(x):
#     return 2 * x       # turunan

# print(newton_raphson(f,1))