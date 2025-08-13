// /**
//  * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
//  */
// const lineConfig = {
//   type: 'line',
//   data: 
//   {
//     labels: ['Hito 1', 'Hito 2', 'Hito 3', 'Hito 4', 'Hito 5', 'Hito 6', 'Hito 7'],
//     datasets: [
//       {
//         label: 'Serie 1',
//         /**
//          * These colors come from Tailwind CSS palette
//          * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
//          */
//         backgroundColor: '#0694a2',
//         borderColor: '#0694a2',
//         data: [43, 48, 40, 54, 67, 73, 70],
//         fill: false,
//       },
//       {
//         label: 'Serie 2',
//         fill: false,
//         /**
//          * These colors come from Tailwind CSS palette
//          * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
//          */
//         backgroundColor: '#7e3af2',
//         borderColor: '#7e3af2',
//         data: [24, 50, 64, 74, 52, 51, 65],
//       },
//     ],
//   },
//   options: {
//     responsive: true,
//     /**
//      * Default legends are ugly and impossible to style.
//      * See examples in charts.html to add your own legends
//      *  */
//     legend: {
//       display: false,
//     },
//     tooltips: {
//       mode: 'index',
//       intersect: false,
//     },
//     hover: {
//       mode: 'nearest',
//       intersect: true,
//     },
//     scales: {
//       x: {
//         display: true,
//         scaleLabel: {
//           display: true,
//           labelString: 'Fecha',
//         },
//       },
//       y: {
//         display: true,
//         scaleLabel: {
//           display: true,
//           labelString: 'Número de Registros',
//         },
//       },
//     },
//   },
// }

// // change this to the id of your chart element in HMTL
// const lineCtx = document.getElementById('line')
// window.myLine = new Chart(lineCtx, lineConfig)
const dynamicData = window.chartData || {
  labels: ['Sin datos'],
  data: [0]
};

console.log('Datos recibidos:', dynamicData); 

const lineConfig = {
  type: 'line',
  data: {
    labels: dynamicData.labels,
    datasets: dynamicData.datasets ? dynamicData.datasets.map(dataset => ({
      label: dataset.label,
      backgroundColor: dataset.backgroundColor,
      borderColor: dataset.borderColor,
      data: dataset.data,
      fill: false,
      tension: 0.1,
    })) : [
      {
        label: 'Registros por día',
        backgroundColor: '#0694a2',
        borderColor: '#0694a2',
        data: dynamicData.data || [0],
        fill: false,
        tension: 0.1,
      }
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: dynamicData.datasets ? true : false,
        position: 'top',
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Fecha',
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Número de Registros',
        },
        beginAtZero: true,
      },
    },
  },
}

const lineCtx = document.getElementById('line')
if (lineCtx) {
  window.myLine = new Chart(lineCtx, lineConfig)
} 