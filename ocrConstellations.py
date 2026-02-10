import easyocr

reader = easyocr.Reader(["en"])

def getText(src: str):
    result = reader.readtext(src, detail=0)
    return result
