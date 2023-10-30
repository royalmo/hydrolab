async function fetchAddressForSensor(lat, lon) {
  const response = await fetch('/get_addresses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ lat, lon }),
  });

  if (response.ok) {
    const result = await response.json();
    const address = result.address.features[0].properties 
    const addr = {
      country: address.country,
      city: address.city,
      street: address.street,
    }
    return addr;
  } else {
    return "Address not available";
  }
}

function updateAddresses() {
  const sensorElements = document.querySelectorAll('tr[id^="sensor-"]');

  sensorElements.forEach(async (sensorElement) => {
    const lat = sensorElement.getAttribute('data-sensorLatitude')
    const lon = sensorElement.getAttribute('data-sensorLongitude')

    const addressCell = sensorElement.querySelector('.address-cell');
    const address = await fetchAddressForSensor(lat, lon);
    addressCell.textContent = address.street + ", " + address.city + ", " + address.country;
  });
}

// Call the updateAddresses function when the page is loaded
window.addEventListener('load', updateAddresses);
