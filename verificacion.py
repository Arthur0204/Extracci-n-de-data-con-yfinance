import yfinance as yf
import json

def info_ticker(ticker):
    print("Verificando si el ticker es válido, espere por favor...")
    try:
        info = yf.Ticker(ticker).info

        # Verificamos que haya información válida
        if not info or 'longName' not in info:
            resultado = "no válido"
            respuesta = f"el Ticker {ticker} no es válido o no hay información del mismo"
            return respuesta, resultado

        #cuando la información es válida, se obtiene los datos:
        nombre = info.get('longName')
        bolsa = info.get('exchange', 'Bolsa desconocida')

                # Cargar y traducir tipo de activo desde JSON externo
        with open('tipos_activos.json', 'r',encoding='utf-8') as file:
            tipos_activo = json.load(file)
        quote_type = info.get('quoteType', '').upper()
        tipo = tipos_activo.get(quote_type, 'Otro')


        respuesta = f"""el ticker: {ticker} es válido
el nombre completo de la empresa/activo es: {nombre}
y corresponde al mercado: {bolsa}"""
        resultado = "valido"
        return respuesta, resultado, nombre, bolsa, tipo

    except Exception as e:
        return {'ticker': ticker, 'valido': False, 'motivo': str(e)}

#print(info_ticker('AAPL')) #esto es para hacer pruebas


