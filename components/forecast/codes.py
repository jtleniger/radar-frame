from components.forecast.icon import get_icon_as_png

def code_to_string(code):
    if code == 0 or code == 1:
        return 'clear'
    if code == 2:
        return 'cloudy'
    if code == 3:
        return 'overcast'
    if code > 40 and code < 50:
        return 'fog'
    if code == 51 or code == 53 or code == 55:
        return 'drizzle'
    if code == 56 or code == 57:
        return 'sleet'
    if code == 61 or code == 80:
        return 'rain'
    if code == 63 or code == 81:
        return 'rain'
    if code == 65 or code == 82:
        return 'rain'
    if code == 66 or code == 67:
        return 'rain'
    if code == 71 or code == 85:
        return 'snow'
    if code == 73:
        return 'snow'
    if code == 75 or code == 86:
        return 'snow'
    if code == 77:
        return 'graupel'
    if code > 94 and code < 100:
        return 'tstorm'
    
    return str(code)

def code_to_img(code, nightime, size):
    icon = 'wi-na'

    if code == 0 or code == 1:
        icon = 'wi-stars' if nightime else 'wi-day-sunny'
    if code == 2:
        icon = 'wi-night-alt-cloudy' if nightime else 'wi-day-cloudy'
    if code == 3:
        icon = 'wi-cloudy'
    if code > 40 and code < 50:
        icon = 'wi-fog'
    if code == 51 or code == 53 or code == 55:
        icon = 'wi-night-alt-showers' if nightime else 'wi-day-showers'
    if code == 56 or code == 57:
        icon = 'wi-night-alt-sleet' if nightime else 'wi-day-sleet'
    if code == 61 or code == 80 or code == 63 or code == 81 or code == 65 or code == 82:
        icon = 'wi-night-alt-rain' if nightime else 'wi-day-rain'
    if code == 66 or code == 67:
        icon = 'wi-night-alt-sleet' if nightime else 'wi-day-sleet'
    if code == 71 or code == 85 or code == 73 or code == 75 or code == 86:
        icon = 'wi-night-snow' if nightime else 'wi-day-snow'
    if code == 77:
        icon = 'wi-night-alt-sleet' if nightime else 'wi-day-sleet'
    if code > 94 and code < 100:
        icon = 'wi-night-alt-thunderstorm' if nightime else 'wi-day-thunderstorm'
    
    return get_icon_as_png(icon, size)