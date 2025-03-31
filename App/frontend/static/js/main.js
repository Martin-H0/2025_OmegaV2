// Inicializace mapy
let map = L.map('map').setView([49.8, 15.5], 7); // Výchozí pohled na ČR
let marker = null;

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Funkce pro formátování čísla jako měnu
function formatPrice(price) {
    return new Intl.NumberFormat('cs-CZ', { 
        style: 'currency', 
        currency: 'CZK',
        maximumFractionDigits: 0
    }).format(price);
}

// Event handler pro kliknutí na mapu
map.on('click', function(e) {
    const lat = e.latlng.lat;
    const lon = e.latlng.lng;
    
    // Aktualizace nebo vytvoření markeru
    if (marker) {
        marker.setLatLng(e.latlng);
    } else {
        marker = L.marker(e.latlng).addTo(map);
    }
    
    // Aktualizace skrytých polí formuláře
    document.getElementById('lat').value = lat;
    
    document.getElementById('lon').value = lon;
    console.log(lat);
    console.log(lon);


    // Aktualizace informací o poloze
    document.getElementById('location-info').innerHTML = `
        <p><strong>Vybraná pozice:</strong> ${lat.toFixed(5)}, ${lon.toFixed(5)}</p>
    `;
    
    // Povolení tlačítka pro odhad
    document.getElementById('predict-button').disabled = false;
    document.getElementById('location-warning').style.display = 'none';
});

// Odeslání formuláře
document.getElementById('property-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Validace formuláře
    const formData = {
        new: parseInt(document.getElementById('new').value),
        area: parseFloat(document.getElementById('area').value),
        room_number: parseInt(document.getElementById('room_number').value),
        kitchen_number: parseInt(document.getElementById('kitchen_number').value),
        lat: parseFloat(document.getElementById('lat').value),
        lon: parseFloat(document.getElementById('lon').value)
    };
    
    // Validace hodnot
    if (!formData.lat || !formData.lon) {
        alert('Prosím, vyberte polohu nemovitosti na mapě.');
        return;
    }
    
    if (formData.area <= 0) {
        alert('Plocha musí být větší než 0.');
        return;
    }
    
    if (formData.room_number < 0) {
        alert('Počet pokojů nemůže být záporný.');
        return;
    }
    
    if (formData.kitchen_number < 0) {
        alert('Počet kuchyní nemůže být záporný.');
        return;
    }
    
    // Zobrazení načítání
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result-section').style.display = 'none';
    
    // Odeslání dat na server
    console.log(formData);
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
        
    })
    .then(response => response.json())
    .then(data => {
        // Skrytí načítání
        document.getElementById('loading').style.display = 'none';
        
        if (data.error) {
            alert('Chyba: ' + data.error);
            return;
        }
        
        // Zobrazení výsledkuzjisti_kraj
        document.getElementById('price-result').textContent = formatPrice(data.predicted_price);
        
        // Aktualizace informací v detailech
        document.getElementById('result-new').textContent = formData.new === 1 ? 'Ano' : 'Ne';
        document.getElementById('result-area').textContent = formData.area;
        document.getElementById('result-room').textContent = formData.room_number;
        document.getElementById('result-kitchen').textContent = formData.kitchen_number;
        
        document.getElementById('result-kraj').textContent = `${data.nazev_kraje} (kód: ${data.kraj_kod})`;
        document.getElementById('result-mesto').textContent = `${data.nazev_velkeho_mesta} (kód: ${data.kod_velkeho_mesta})`;
        document.getElementById('result-vzdalenost').textContent = data.vzdalenost_centrum_km;
        document.getElementById('result-je-velke-mesto').textContent = data.je_velke_mesto === 1 ? 'Ano' : 'Ne';
        
        // Zobrazení sekce s výsledkem
        document.getElementById('result-section').style.display = 'block';
        
        // Plynulé scrollování k výsledku
        document.getElementById('result-section').scrollIntoView({
            behavior: 'smooth'
        });
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        alert('Chyba při komunikaci se serverem: ' + error);
    });
});