// weather app

function toTextualDescription(degree) {
	if (degree > 337.5) return 'N';
	if (degree > 292.5) return 'NW';
	if (degree > 247.5) return 'W';
	if (degree > 202.5) return 'SW';
	if (degree > 157.5) return 'S';
	if (degree > 122.5) return 'SE';
	if (degree > 67.5) return 'E';
	if (degree > 22.5) {
		return 'NE';
	}
	return 'N';
}

// https://stackoverflow.com/questions/36475255/i-have-wind-direction-data-coming-from-openweathermap-api-and-the-data-is-repre

async function getLaconiaWeather() {
	const url = `https://api.openweathermap.org/data/2.5/weather?zip=03246,us&appid=16fd7721aa7d49db8f58e9dfa71e1f87&units=imperial`;

	const $weatherIcon = $('#weather-icon');
	const $temperature = $('#temperature');
	const $weatherDesc = $('#weather-description');
	try {
		const res = await axios.get(url);
		console.log(res);
		const description = res.data.weather[0].description;
		const icon = res.data.weather[0].icon;
		const temp = Math.round(res.data.main.temp);
		const windSpeed = res.data.wind.speed * 0.868976;
		const windDir = toTextualDescription(res.data.wind.deg);
		$weatherIcon.append(`<img id='weather-icon' src=http://openweathermap.org/img/wn/${icon}@2x.png>`);
		$temperature.append(`<span class="temp"> ${temp}&#176F </span>`);
		$weatherDesc.append(
			`<span class="weather-desc"> ${description} <br> <i class="fa-light fa-wind"></i> ${windSpeed.toFixed(
				2
			)} <span class="mph">kts,</span> ${windDir.toUpperCase()}`
		);
	} catch (e) {
		$weatherIcon.append('<i class="fa-solid fa-circle-exclamation"></i>');
		$weatherDesc.append('Weather unavailable');
	}
}

$(document).ready(getLaconiaWeather());

const $payNow = $('#pay-now');
const $paySpinner = $('#pay-spinner');
const $payBtn = $('#pay-submit');

$paySpinner.hide();

$payBtn.click(function() {
	$payNow.hide();
	$paySpinner.show();
});
