
function handleFile(filePath) {
    console.log(filePath);
    fetch(filePath)
      .then(response => response.text())
      .then(content => {
        const rows = content.split('\n');
        const headers = rows[0].split(',');

        let tableHTML = '<table class="container"><thead><tr>';
        headers.forEach(header => {
          tableHTML += `<th>${header}</th>`;
        });
        tableHTML += '</tr></thead>';

        for (let i = 1; i < rows.length; i++) {
          const cells = rows[i].split(',');
          tableHTML += '<tr>';
          cells.forEach(cell => {
            tableHTML += `<td>${cell}</td>`;
          });
          tableHTML += '</tr>';
        }

        tableHTML += '</table>';
        document.getElementById('tableContainer').innerHTML = tableHTML;
      })
      .catch(error => console.error('Error loading file:', error));
  }
const selectBlock = (block) =>{
    document.querySelector('.top-line').innerHTML=block;
    const fp=`${block}.csv`
    console.log(fp);
    handleFile(fp);
    
}