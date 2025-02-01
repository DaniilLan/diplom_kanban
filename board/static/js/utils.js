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