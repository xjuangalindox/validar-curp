# CONFIGURAR PYTHON
# _______________________________________________________________________

## 1. Crear y activar entorno virtual (desde la raíz del proyecto)
```bash
python -m venv venv
venv/Scripts/activate
```

## 2. Instalar librerías necesarias
```bash
python -m pip install PyMuPDF
python -m pip install pytesseract pillow
python -m pip install PyMuPDF pytesseract pillow
```
## 3. Comprovar que fitz ya funciona
```bash
python -c "import fitz; print(fitz.__doc__)"
```

Nota: warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
Comprobar 3 librerias: python -c "import fitz, pytesseract, PIL; print('Todo instalado correctamente')"



## Verificar si esta instalado Tesseract-OCR
Test-Path "C:\Program Files\Tesseract-OCR\tesseract.exe"

## Instalar Tesseract-OCR
https://github.com/UB-Mannheim/tesseract/wiki?utm_source=chatgpt.com
tesseract-ocr-w64-setup-5.5.3.20260724.exe (64 bit)

NOTA:
La ubicación predeterminada debería ser: C:\Program Files\Tesseract-OCR\
y dentro debe quedar: C:\Program Files\Tesseract-OCR\tesseract.exe

## Comprobar instalacion
Test-Path "C:\Program Files\Tesseract-OCR\tesseract.exe"
tesseract --version

## Paso 1. Descargar el idioma español
https://github.com/tesseract-ocr/tessdata/raw/refs/heads/main/spa.traineddata
archivo: spa.traineddata
C:\Program Files\Tesseract-OCR\tessdata

## Verificar que se haya agregado el idioma
Test-Path "C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata"
True

## Paso 4. Verificar que Tesseract reconoce el español
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs

NOTA:
List of available languages in "C:\Program Files\Tesseract-OCR\tessdata/" (2):
eng
spa











## 3. Ejecutar el script principal
```bash
python app.py
```
