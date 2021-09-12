# import the module
import python_weather
import asyncio
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
import customStyleSheet as cs

_current, _forecasts = None, None

async def getweather(city='Munich'):
    # declare the client. format defaults to the metric system (celcius, km/h, etc.)
    client = python_weather.Client()
    # fetch a weather forecast from a city
    weather = await client.find(city)
    # returns the current day's forecast temperature (int)
    current = weather.current
    # get the weather forecast for a few days
    forecasts = weather.forecasts
    # close the wrapper once done
    await client.close()
    return current, forecasts

def weatherEvent(city='Munich'):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(getweather(city))
    

class SingleWeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.weatherBtn = QPushButton(self)
        self.weatherBtn.setStyleSheet(cs.widget_icon_style)
        self.weatherLabel = QLabel(self.weatherBtn)
        self.weatherLabel.setStyleSheet(cs.widget_label_style)
        self.weatherLabel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.weatherLabel.setTextFormat(Qt.RichText);
        self.weatherLabel.move(self.weatherBtn.width()+40, self.weatherBtn.y()+2)
        self.updateWeather()

    def updateWeather(self):
        print('updating weather...')
        cur_sky = _current.sky_text
        cur_temp = _current.temperature
        cur_time = int(str(_current.date).split(' ')[1].split(':')[0])
        splitted_sky = cur_sky.split(' ')
        self.weatherBtn.setIcon(getWeatherIcon(cur_time, cur_sky))
        if len(splitted_sky) == 1:
            self.weatherLabel.setText(f"<p style='font-size:38px;margin-bottom: 0px;'>{cur_temp}°</p><p style='font-size:18px;margin-top:0px;'>{cur_sky}</p>");
        else:
            self.weatherLabel.setText(f"<p style='font-size:38px;margin-bottom: 0px;'>{cur_temp}°</p><p style='font-size:18px;margin-top:0px;line-height:0.85;'>{splitted_sky[0]}<br>{splitted_sky[1]}</p>");
    
    def sizeHint(self):
        return QSize(240, 120)
    def minimumSizeHint(self):
        return QSize(240, 120)


class MultiWeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.locationLabel = QLabel(_current.observation_point, self)
        self.locationLabel.setStyleSheet(cs.time_label_style)
        self.locationLabel.move(self.locationLabel.x()-13, self.locationLabel.y()+5)
        self.labels = []
        next_y = 0
        for i in range(0, 5):
            label_day = QLabel(self)
            label_txt = QLabel(self)
            label_day.setStyleSheet(cs.long_widget_label_style)
            label_icon = QLabel(self)
            label_txt.setStyleSheet('color: #F8F8FF;padding: 10px;min-width:330px;max-width:350px;min-height:48px;max-height:48px;background-color:none;')
            for label in [label_day, label_txt]:
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                label.setTextFormat(Qt.RichText);
            next_y = next_y + 48
            label_day.move(label_day.x(), next_y)
            label_icon.move(label_icon.x() + 96, next_y + 16)
            label_txt.move(label_txt.x() + 132, next_y)
            self.labels.append((label_day, label_txt, label_icon))
        self.updateWeather()
    
    def updateWeather(self):
        print('updating forecasts...')
        for i in range(0, 5):
            forecast = _forecasts[i]
            forc_low = forecast.low
            forc_high = forecast.high
            forc_precip = forecast.precip
            forc_day = forecast.short_day
            forc_sky = forecast.sky_text
            splitted_sky = forc_sky.split(' ')
            if i == 0:
                forc_day = 'Today'
            if not forc_precip:
                forc_precip = 0
            self.labels[i][0].setText(f"<span style='font-size:24px;white-space:pre-wrap;'>{forc_day}</span>")
            self.labels[i][1].setText(f"<span style='font-size:24px;color:dimgray;white-space:pre-wrap'>{forc_low}°   </span><span style='font-size:24px;white-space:pre-wrap'>{forc_high}°   </span><span style='font-size:18px;'>{forc_sky}</span>")
            self.labels[i][2].setPixmap(getWeatherIcon(6, forc_sky).pixmap(QSize(36, 36)))

    def sizeHint(self):
        return QSize(420, 320)
    def minimumSizeHint(self):
        return QSize(420, 320)

    

class WeatherWidget(QWidget):
    def __init__(self):
         super().__init__()
         global _current, _forecasts
         _current, _forecasts = weatherEvent('Munich')
         #self.locationLabel = QLabel(self)
         self.cur_weather = SingleWeatherWidget()
         self.multi_weather = MultiWeatherWidget()
         #self.locationLabel.setStyleSheet(cs.time_label_style)
         #self.locationLabel.setText(_current.observation_point)
         self.cur_weather.weatherBtn.clicked.connect(self.btnOnClick)
         self.multi_weather.setVisible(False)
         vlayout = QVBoxLayout()
         #vlayout.addWidget(self.locationLabel)
         vlayout.addWidget(self.cur_weather)
         vlayout.addWidget(self.multi_weather)
         vlayout.addStretch()
         vlayout.setSpacing(10)
         self.setLayout(vlayout)
         timer = QTimer(self)
         timer.timeout.connect(self.updateAllWeather)
         timer.start(1800000)
    
    def btnOnClick(self):
        self.multi_weather.setVisible(not self.multi_weather.isVisible())

    def updateAllWeather(self):
        global _current, _forecasts
        _current, _forecasts = weatherEvent('Munich')
        self.cur_weather.updateWeather()
        self.multi_weather.updateWeather()

def getWeatherIcon(cur_time, cur_sky):
    if cur_time >= 6 and cur_time <= 18:
        if 'Sunny' == cur_sky or 'Clear' in cur_sky:
            return QIcon('../image/weather/sunny.png')
        elif 'Sunny' in cur_sky:
            return QIcon('../image/weather/partly_sunny.png')
        elif 'Rain' in cur_sky or 'Showers' in cur_sky:
            return QIcon('../image/weather/day_rain.png')
        elif 'Cloudy' in cur_sky:
            return QIcon('../image/weather/day_cloudy.png')
        else:
            return QIcon('../image/weather/unknown_weather.png')
    else: 
        if 'Rain' in cur_sky or 'Showers' in cur_sky:
            return QIcon('../image/weather/cloudy_rain.png')
        elif 'Cloudy' in cur_sky or 'Clear' in cur_sky:
            return QIcon('../image/weather/night_cloudy.png')
        else:
            return QIcon('../image/weather/unknown_weather.png')

def printWeather():
    current, forecasts = weatherEvent()
    #print current
    print(current.sky_text, current.temperature)
    #print forecast
    for forecast in forecasts:
        print(str(forecast.date), forecast.sky_text, forecast.temperature)

if __name__ == "__main__":
    #printWeather()
    app = QApplication(sys.argv)
    ex = WeatherWidget()
    ex.show()
    sys.exit(app.exec_())
