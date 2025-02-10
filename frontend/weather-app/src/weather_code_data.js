export const WEATHER_CODE = {
    'thunderstrom': {
        200: 'thunderstorm with light rain',
        201: 'thunderstorm with rain',
        202: 'thunderstorm with heavy rain',
        210: 'light thunderstorm',
        211: 'thunderstorm',
        212: 'heavy thunderstorm',
        221: 'ragged thunderstorm',
        230: 'thunderstorm with light drizzle',
        231: 'thunderstorm with drizzle',
        232: 'thunderstorm with heavy drizzle',
    },
    'drizzle': {
        300: 'light intensity drizzle',
        301: 'drizzle',
        302: 'heavy intensity drizzle',
        310: 'light intensity drizzle rain',
        311: 'drizzle rain',
        312: 'heavy intensity drizzle rain',
        313: 'shower rain and drizzle',
        314: 'heavy shower rain and drizzle',
        321: 'shower drizzle',
    },
    'rain' : {
        500: 'light rain',
        501: 'moderate rain',
        502: 'heavy intensity rain',
        503: 'very heavy rain',
        504: 'extreme rain',
        511: 'freezing rain',
        520: 'light intensity shower rain',
        521: 'shower rain',
        522: 'heavy intensity shower rain',
        531: 'ragged shower rain',
    },
    'snow': {
        600: 'light snow',
        601: 'snow',
        602: 'heavy snow',
        611: 'sleet',
        612: 'light shower sleet',
        613: 'shower sleet',
        615: 'light rain and snow',
        616: 'rain and snow',
        620: 'light shower snow',
        621: 'shower snow',
        622: 'heavy shower snow',
    },
    'atmosphere': {
        701: 'Mist',	
        711: 'Smoke',
        721: 'Haze',
        731: 'Dust',
        741: 'Fog',
        751: 'Sand',
        761: 'Dust',
        762: 'Volcanic Ash',
        771: 'Squall',
        781: 'Tornado',
    },
    'clear': {
        800: 'clear sky',
    },
    'clouds': {
        801: 'few clouds', //11-25%
        802: 'scattered clouds', //25-50%
        803: 'broken clouds', //51-84%
        804: 'overcast clouds' // 85-100%
    }
}