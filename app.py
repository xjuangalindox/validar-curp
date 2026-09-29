import re
import fitz
import pytesseract
from PIL import Image
import io
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

CARPETA = "."


# Si Tesseract no está en el PATH de Windows,
# descomenta esta línea y modifica la ruta:
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ============================================================
# EXTRAER TEXTO DE UN PDF
# ============================================================

def extraer_texto_pdf(ruta_pdf):

    documento = fitz.open(ruta_pdf)

    texto = ""

    for pagina in documento:
        texto += pagina.get_text()

    documento.close()

    return texto


# ============================================================
# OCR DE UN PDF ESCANEADO
# ============================================================

def hacer_ocr_pdf(ruta_pdf):

    documento = fitz.open(ruta_pdf)

    texto = ""

    for numero, pagina in enumerate(documento):

        print(f"  OCR página {numero + 1}...")

        # Convertimos PDF -> imagen
        pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))

        imagen = Image.open(
            io.BytesIO(pix.tobytes("png"))
        )

        # OCR
        texto += pytesseract.image_to_string(
            imagen,
            lang="spa"
        )

    documento.close()

    return texto


# ============================================================
# BUSCAR CURP
# ============================================================

def buscar_curp(texto):

    texto = texto.upper()

    # Quitamos espacios, saltos de línea, etc.
    texto = re.sub(r"[^A-Z0-9]", "", texto)

    # CURP = 18 caracteres
    patron = r"[A-Z]{4}[0-9]{6}[A-Z]{6}[A-Z0-9][0-9]"

    resultado = re.search(patron, texto)

    if resultado:
        return resultado.group()

    return None


# ============================================================
# OBTENER CURP DE RENAPO
# ============================================================

def obtener_curp_renapo(ruta_pdf):

    print("\nLeyendo CURP de RENAPO...")

    texto = extraer_texto_pdf(ruta_pdf)

    curp = buscar_curp(texto)

    return curp


# ============================================================
# OBTENER CURP DE CUALQUIER DOCUMENTO
# ============================================================

def obtener_curp_documento(ruta_pdf):

    print("\n----------------------------------------")
    print("Documento:", os.path.basename(ruta_pdf))
    print("----------------------------------------")

    # -------------------------------------
    # Primero intentamos texto normal
    # -------------------------------------

    print("Buscando texto...")

    texto = extraer_texto_pdf(ruta_pdf)

    curp = buscar_curp(texto)

    if curp:

        print("CURP encontrada en texto.")

        return curp

    # -------------------------------------
    # Si no hay texto, usamos OCR
    # -------------------------------------

    print("No se encontró CURP en texto.")
    print("Intentando OCR...")

    texto = hacer_ocr_pdf(ruta_pdf)

    curp = buscar_curp(texto)

    if curp:

        print("CURP encontrada mediante OCR.")

        return curp

    print("No se encontró CURP.")

    return None


# ============================================================
# COMPARAR
# ============================================================

def comparar_curp(curp_renapo, curp_documento):

    if curp_documento is None:

        return "NO ENCONTRADA"

    if curp_renapo == curp_documento:

        return "COINCIDE"

    else:

        return "NO COINCIDE"


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("==============================================")
    print("          VALIDACIÓN DE CURP")
    print("==============================================")

    # -----------------------------------------
    # Buscar automáticamente el PDF de CURP
    # -----------------------------------------

    archivo_renapo = None

    for archivo in os.listdir(CARPETA):

        if archivo.lower().endswith(".pdf"):

            if "CURP" in archivo.upper():

                archivo_renapo = archivo
                break

    if archivo_renapo is None:

        print("No encontré el PDF de CURP de RENAPO.")
        return


    # -----------------------------------------
    # Obtener CURP de RENAPO
    # -----------------------------------------

    ruta_renapo = os.path.join(
        CARPETA,
        archivo_renapo
    )

    curp_renapo = obtener_curp_renapo(
        ruta_renapo
    )


    if curp_renapo is None:

        print("\nERROR:")
        print("No pude encontrar la CURP en RENAPO.")
        return


    print("\n==============================================")
    print("CURP DE RENAPO:")
    print(curp_renapo)
    print("==============================================")


    # -----------------------------------------
    # Revisar todos los demás PDFs
    # -----------------------------------------

    resultados = []

    for archivo in os.listdir(CARPETA):

        # Solo PDFs
        if not archivo.lower().endswith(".pdf"):
            continue

        # No volver a revisar RENAPO
        if archivo == archivo_renapo:
            continue


        ruta = os.path.join(
            CARPETA,
            archivo
        )

        curp_documento = obtener_curp_documento(
            ruta
        )

        resultado = comparar_curp(
            curp_renapo,
            curp_documento
        )

        resultados.append(
            (archivo, curp_documento, resultado)
        )


    # =========================================
    # RESULTADOS FINALES
    # =========================================

    print("\n\n")
    print("==============================================")
    print("              RESULTADOS")
    print("==============================================")

    for archivo, curp, resultado in resultados:

        print("\nDocumento:")
        print(archivo)

        print("CURP encontrada:")
        print(curp)

        print("Resultado:")
        print(resultado)

        print("----------------------------------------------")


    print("\n==============================================")
    print("             VALIDACIÓN TERMINADA")
    print("==============================================")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    main()
