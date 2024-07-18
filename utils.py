import requests
from datetime import datetime
from requests.exceptions import RequestException, HTTPError, Timeout

class InputValidator:
    """Clase para validar las entradas del usuario."""

    @staticmethod
    def validate_sign(sign: str) -> bool:
        valid_signs = {
            "aries", "taurus", "gemini", "cancer", "leo", "virgo",
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
        }
        if sign.lower() not in valid_signs:
            raise ValueError("Signo zodiacal no válido.")
        return True

    @staticmethod
    def validate_day(day: str) -> bool:
        valid_days = {"TODAY", "TOMORROW", "YESTERDAY"}
        if day.upper() not in valid_days:
            try:
                datetime.strptime(day, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de fecha no válido. Debe ser YYYY-MM-DD o uno de: TODAY, TOMORROW, YESTERDAY.")
        return True


class HttpClient:
    """Clase para realizar solicitudes HTTP."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str, params: dict, timeout: int = 10) -> dict:
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except (HTTPError, Timeout) as http_err:
            raise SystemError(f"Error en la solicitud HTTP: {http_err}")
        except RequestException as req_err:
            raise SystemError(f"Error en la solicitud: {req_err}")


class HoroscopeService:
    """Clase para manejar la lógica del horóscopo."""

    def __init__(self, client: HttpClient):
        self.client = client

    def get_daily_horoscope(self, sign: str, day: str) -> dict:
        InputValidator.validate_sign(sign)
        InputValidator.validate_day(day)
        endpoint = "/api/v1/get-horoscope/daily"
        params = {"sign": sign, "day": day}
        return self.client.get(endpoint, params)


# Controlador principal que utiliza las clases anteriores
def obtain_daily_horoscope(sign: str, day: str) -> dict:
    base_url = "https://horoscope-app-api.vercel.app"
    client = HttpClient(base_url)
    service = HoroscopeService(client)

    return service.get_daily_horoscope(sign, day)