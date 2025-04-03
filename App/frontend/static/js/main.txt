document.addEventListener("DOMContentLoaded", function() {
    // Check if we're on the estimate page by looking for the map element
    const mapElement = document.getElementById("map");
    if (!mapElement) return;
    
    // Initialize map
    const map = L.map("map").setView([49.8, 15.5], 7);
  
    // Add OpenStreetMap layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
  
    // Variables for marker
    let marker = null;
  
    // Set click event on map
    map.on("click", function(e) {
      const lat = e.latlng.lat;
      const lon = e.latlng.lng;
  
      // Update hidden inputs
      document.getElementById("lat").value = lat;
      document.getElementById("lon").value = lon;
  
      // Update displayed coordinates
      document.getElementById(
        "coordinates"
      ).textContent = `Souřadnice: ${lat.toFixed(6)}, ${lon.toFixed(6)}`;
  
      // Remove previous marker if exists
      if (marker) {
        map.removeLayer(marker);
      }
  
      // Add new marker
      marker = L.marker(e.latlng).addTo(map);
      marker.bindPopup("Vybraná lokace").openPopup();
    });
  
    // Handle calculate button
    document
      .getElementById("calculateBtn")
      .addEventListener("click", function() {
        // Form validation
        const new_property = document.getElementById("new").value;
        const area = document.getElementById("area").value;
        const room_number = document.getElementById("room_number").value;
        const kitchen_number = document.getElementById("kitchen_number").value;
        const lat = document.getElementById("lat").value;
        const lon = document.getElementById("lon").value;
  
        // Check if all fields are filled
        if (!area || !room_number || !kitchen_number || !lat || !lon) {
          alert(
            "Prosím vyplňte všechny údaje a vyberte lokaci na mapě kliknutím."
          );
          return;
        }
  
        // Show loading state
        const calculateBtn = document.getElementById("calculateBtn");
        const originalText = calculateBtn.textContent;
        calculateBtn.disabled = true;
        calculateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Zpracovávám...';
  
        // Prepare data for sending
        const data = {
          new: parseInt(new_property),
          area: parseFloat(area),
          room_number: parseInt(room_number),
          kitchen_number: parseInt(kitchen_number),
          lat: parseFloat(lat),
          lon: parseFloat(lon)
        };
  
        // Send POST request to API endpoint
        fetch("/predict", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        })
          .then(response => {
            if (!response.ok) {
              throw new Error("Chyba při komunikaci se serverem");
            }
            return response.json();
          })
          .then(result => {
            // Display result
            document.getElementById("resultCard").style.display = "block";
            document.getElementById(
              "predictedPrice"
            ).textContent = `${result.predicted_price.toLocaleString()} Kč`;
            document.getElementById("regionName").textContent = result.nazev_kraje;
            document.getElementById("regionCode").textContent = result.kraj_kod;
            document.getElementById("cityName").textContent =
              result.nazev_velkeho_mesta;
            document.getElementById("cityCode").textContent =
              result.kod_velkeho_mesta;
            document.getElementById(
              "distanceCenter"
            ).textContent = result.vzdalenost_centrum_km;
            document.getElementById("isBigCity").textContent =
              result.je_velke_mesto === 1 ? "Ano" : "Ne";
  
            // Scroll to result
            document.getElementById("resultCard").scrollIntoView({
              behavior: "smooth"
            });
            
            // Reset button
            calculateBtn.disabled = false;
            calculateBtn.textContent = originalText;
          })
          .catch(error => {
            console.error("Chyba:", error);
            alert("Nastala chyba při zpracování požadavku: " + error.message);
            
            // Reset button
            calculateBtn.disabled = false;
            calculateBtn.textContent = originalText;
          });
      });
  });
  



// document.addEventListener("DOMContentLoaded", function() {
//     // Inicializace mapy
//     const map = L.map("map").setView([49.8, 15.5], 7);
  
//     // Přidání OpenStreetMap podkladu
//     L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//       attribution:
//         '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//     }).addTo(map);
  
//     // Proměnné pro marker
//     let marker = null;
  
//     // Nastavení události kliknutí na mapu
//     map.on("click", function(e) {
//       const lat = e.latlng.lat;
//       const lon = e.latlng.lng;
  
//       // Aktualizace skrytých inputů
//       document.getElementById("lat").value = lat;
//       document.getElementById("lon").value = lon;
  
//       // Aktualizace zobrazeného textu se souřadnicemi
//       document.getElementById(
//         "coordinates"
//       ).textContent = `Souřadnice: ${lat.toFixed(6)}, ${lon.toFixed(6)}`;
  
//       // Odstranění předchozího markeru, pokud existuje
//       if (marker) {
//         map.removeLayer(marker);
//       }
  
//       // Přidání nového markeru
//       marker = L.marker(e.latlng).addTo(map);
//       marker.bindPopup("Vybraná lokace").openPopup();
//     });
  
//     // Obsluha tlačítka pro výpočet odhadu
//     document
//       .getElementById("calculateBtn")
//       .addEventListener("click", function() {
//         // Validace formuláře
//         const new_property = document.getElementById("new").value;
//         const area = document.getElementById("area").value;
//         const room_number = document.getElementById("room_number").value;
//         const kitchen_number = document.getElementById("kitchen_number").value;
//         const lat = document.getElementById("lat").value;
//         const lon = document.getElementById("lon").value;
  
//         // Kontrola, zda jsou všechna pole vyplněna
//         if (!area || !room_number || !kitchen_number || !lat || !lon) {
//           alert(
//             "Prosím vyplňte všechny údaje a vyberte lokaci na mapě kliknutím."
//           );
//           return;
//         }
  
//         // Příprava dat pro odeslání
//         const data = {
//           new: parseInt(new_property),
//           area: parseFloat(area),
//           room_number: parseInt(room_number),
//           kitchen_number: parseInt(kitchen_number),
//           lat: parseFloat(lat),
//           lon: parseFloat(lon)
//         };
  
//         // Odeslání POST požadavku na API endpoint
//         fetch("/predict", {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json"
//           },
//           body: JSON.stringify(data)
//         })
//           .then(response => {
//             if (!response.ok) {
//               throw new Error("Chyba při komunikaci se serverem");
//             }
//             return response.json();
//           })
//           .then(result => {
//             // Zobrazení výsledku
//             document.getElementById("resultCard").style.display = "block";
//             document.getElementById(
//               "predictedPrice"
//             ).textContent = `${result.predicted_price.toLocaleString()} Kč`;
//             document.getElementById("regionName").textContent = result.nazev_kraje;
//             document.getElementById("regionCode").textContent = result.kraj_kod;
//             document.getElementById("cityName").textContent =
//               result.nazev_velkeho_mesta;
//             document.getElementById("cityCode").textContent =
//               result.kod_velkeho_mesta;
//             document.getElementById(
//               "distanceCenter"
//             ).textContent = result.vzdalenost_centrum_km;
//             document.getElementById("isBigCity").textContent =
//               result.je_velke_mesto === 1 ? "Ano" : "Ne";
  
//             // Scrollování na výsledek
//             document.getElementById("resultCard").scrollIntoView({
//               behavior: "smooth"
//             });
//           })
//           .catch(error => {
//             console.error("Chyba:", error);
//             alert("Nastala chyba při zpracování požadavku: " + error.message);
//           });
//       });
//   });
  