function toggleDetails(element) {
    // Get the details row (next sibling of the clicked arrow's row)
    var detailsRow = element.closest('tr').nextElementSibling;

    // Toggle the display of the details row
    if (detailsRow.style.display === 'none' || detailsRow.style.display === '') {
      detailsRow.style.display = 'table-row';
      element.classList.add('down'); // Rotate arrow to point right
    } else {
      detailsRow.style.display = 'none';
      element.classList.remove('down'); // Rotate arrow to point down
    }
  }