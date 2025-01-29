/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
const lineConfig = {
  type: 'line',
  data: {
    datasets: [
      {
        label: 'Respuestas por día',
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: 'rgba(6, 148, 162, 0.2)',
        borderColor: '#0694a2',
        pointBackgroundColor: '#0694a2',
        pointBorderColor: '#ffffff',
        data: [], // Inicialmente vacío, se llenará con datos dinámicos
        fill: true,
        tension: 0.3, // Suaviza la línea
      },
    ],
    labels: [], // Inicialmente vacío
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Día',
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Número de respuestas',
        },
        beginAtZero: true,
      },
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
    },
  },
};

// Cambia esto al ID del canvas en tu HTML
const lineCtx = document.getElementById('line');
window.myLine = new Chart(lineCtx, lineConfig);

// Función para procesar el JSON y contar respuestas por día
countResponsesByDay = (data) => {
  let dateCounts = {};

  Object.values(data).forEach(record => {
      const savedTime = record.saved;
      if (!savedTime) return;

      try {
          // Eliminar caracteres extraños y espacios no deseados
          let cleanedTime = savedTime.replace(/\xa0/g, ' ').trim();
          cleanedTime = cleanedTime.replace('a. m.', 'AM').replace('p. m.', 'PM');

          // Extraer solo la parte de la fecha (dd/mm/yyyy)
          const dateMatch = cleanedTime.match(/(\d{2})\/(\d{2})\/(\d{4})/);
          if (!dateMatch) {
              console.warn("No se pudo extraer la fecha de:", savedTime);
              return;
          }

          // Construir la fecha en formato dd/mm/yyyy
          const formattedDate = `${dateMatch[1]}/${dateMatch[2]}/${dateMatch[3]}`;

          // Contar respuestas por día
          dateCounts[formattedDate] = (dateCounts[formattedDate] || 0) + 1;

      } catch (error) {
          console.error("Error procesando fecha:", savedTime, error);
      }
  });

  // Ordenar fechas correctamente
  const sortedDates = Object.keys(dateCounts)
      .map(date => ({
          original: date,
          parsed: new Date(date.split('/').reverse().join('-'))
      }))
      .filter(item => !isNaN(item.parsed)) // Elimina fechas inválidas
      .sort((a, b) => a.parsed - b.parsed)
      .map(item => item.original);

  const counts = sortedDates.map(date => dateCounts[date]);
  console.log("✅ Datos procesados para la gráfica:", sortedDates, counts); // Para depuración

  return { labels: sortedDates, counts };
};



// Función para actualizar la gráfica
update = () => {
  fetch('/api/v1/landing')
    .then(response => response.json())
    .then(data => {
      let { labels, counts } = countResponsesByDay(data);

      if (labels.length === 0 || counts.length === 0) {
        console.warn("No hay datos para mostrar en la gráfica.");
        return;
      }

      // Reset data
      window.myLine.data.labels = [];
      window.myLine.data.datasets[0].data = [];

      // Nuevos datos
      window.myLine.data.labels = [...labels];
      window.myLine.data.datasets[0].data = [...counts];

      window.myLine.update();
    })
    .catch(error => console.error('Error:', error));
};

// Llamar a la función para obtener los datos iniciales
update();

