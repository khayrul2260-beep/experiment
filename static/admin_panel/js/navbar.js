// Basic dashboard JS: populate charts and sample table
document.addEventListener('DOMContentLoaded', ()=> {
  // Line chart (sales)
  const lineCtx = document.getElementById('lineChart').getContext('2d');
  const months = ['Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const salesData = [22000, 35000, 40567, 31000, 43000, 36000, 39000];
  new Chart(lineCtx, {
    type: 'line',
    data: {
      labels: months,
      datasets: [{
        label: 'Sales',
        data: salesData,
        borderColor: '#34d399',
        backgroundColor: 'rgba(52,211,153,0.08)',
        tension: 0.35,
        fill: true,
        pointRadius: 3
      }]
    },
    options: {
      plugins: {legend:{display:false}},
      scales: {
        x:{grid:{display:false},ticks:{color:'#9aa6b2'}},
        y:{grid:{color:'rgba(255,255,255,0.03)'},ticks:{color:'#9aa6b2'}}
      },
      responsive:true,
      maintainAspectRatio:false
    }
  });

  // Donut chart
  const donutCtx = document.getElementById('donutChart').getContext('2d');
  new Chart(donutCtx, {
    type: 'doughnut',
    data: {
      labels:['Social','Purchased','Affiliate','Ad'],
      datasets:[{
        data:[55,25,15,5],
        backgroundColor:['#6ee7b7','#60a5fa','#fbbf24','#f97316'],
        hoverOffset:6
      }]
    },
    options:{plugins:{legend:{display:false}},cutout:'70%'}
  });

  // populate sample orders table
  const orders = [
    {id:2323, name:'Devon Lane', email:'devon@example.com', amount:'$778.35', status:'delivered', date:'07.05.2023'},
    {id:2458, name:'Darrell Steward', email:'darrell@example.com', amount:'$219.78', status:'delivered', date:'03.07.2023'},
    {id:6289, name:'Darlene Robertson', email:'darlene@example.com', amount:'$928.41', status:'cancelled', date:'23.03.2023'},
    {id:3869, name:'Courtney Henry', email:'courtney@example.com', amount:'$90.51', status:'pending', date:'04.07.2023'},
    {id:1247, name:'Eleanor Pena', email:'eleanor@example.com', amount:'$275.43', status:'delivered', date:'10.03.2023'}
  ];
  const tbody = document.getElementById('ordersBody');
  orders.forEach(o=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${o.id}</td>
      <td>${o.name}</td>
      <td>${o.email}</td>
      <td>${o.amount}</td>
      <td><span class="status ${o.status}">${o.status.charAt(0).toUpperCase()+o.status.slice(1)}</span></td>
      <td>${o.date}</td>
    `;
    tbody.appendChild(tr);
  });
});


