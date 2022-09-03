// weather app

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
		$weatherIcon.append(`<img id='weather-icon' src=http://openweathermap.org/img/wn/${icon}@2x.png>`);
		$temperature.append(`<span class="temp"> ${temp}&#176F </span>`);
		$weatherDesc.append(
			`<span class="weather-desc"> ${description} <br> <i class="fa-light fa-wind"></i> ${windSpeed.toFixed(
				2
			)} <span class="mph">knots</span></span>`
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
