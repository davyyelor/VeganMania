import goslate

def traducir(texto, idioma):
    gs = goslate.Goslate()
    traduccion = gs.translate(texto, idioma)
    return traduccion

if __name__ == "__main__":
    print(traducir("Hola mundo", "en"))