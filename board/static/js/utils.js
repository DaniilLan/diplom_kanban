function parseTimeInput(timeInput) {
  const timeUnits = {
    'д': 24 * 60,  // дни в минутах
    'ч': 60,       // часы в минутах
    'м': 1,        // минуты
  };

  let totalMinutes = 0;
  const matches = timeInput.match(/(\d+)([дчм])/g);

  if (matches) {
    matches.forEach(match => {
      const value = parseInt(match);
      const unit = match.slice(-1); // Последний символ (д, ч, м)
      totalMinutes += value * (timeUnits[unit] || 0);
    });
  }

  return totalMinutes;
}

function convertMinutesToTime(minutes) {
    const days = Math.floor(minutes / 1440);
    const hours = Math.floor((minutes % 1440) / 60);
    const mins = minutes % 60;

    let result = '';
    if (days > 0) {
        result += `${days}д `;
    }
    if (hours > 0) {
        result += `${hours}ч `;
    }
    if (mins > 0) {
        result += `${mins}м`;
    }

    if (result === '') {
        result = '0м';
    }
    return result.trim();
}