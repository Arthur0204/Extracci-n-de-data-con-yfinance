import yfinance as yf
import json

def info_ticker(ticker):
    print("Verificando si el ticker es válido, espere por favor...")
    try:
        info = yf.Ticker(ticker).info

        if not info or 'longName' not in info: #verifica si el ticker es válido o existe dentro de los activos disponibles
            resultado = "no válido"
            respuesta = f"el Ticker {ticker} no es válido o no hay información del mismo"
            return respuesta, resultado

        nombre = info.get('longName') #nombre completo del activo
        bolsa = info.get('exchange', 'Bolsa desconocida') #bolsa a la cual pertenece

        with open('tipos_activos.json', 'r',encoding='utf-8') as file: #devuelve el tipo de activo de entre todos los posibles
            tipos_activo = json.load(file)
        quote_type = info.get('quoteType', '').upper()
        tipo = tipos_activo.get(quote_type, 'Otro')

        #respuesta en caso el activo sea válido
        respuesta = f"""el ticker: {ticker} es válido
el nombre completo de la empresa/activo es: {nombre}
y corresponde al mercado: {bolsa}"""
        resultado = "valido"
        return respuesta, resultado, nombre, bolsa, tipo

    except Exception as e: #respuesta en caso de error o exception
        return {'ticker': ticker, 'valido': False, 'motivo': str(e)}


