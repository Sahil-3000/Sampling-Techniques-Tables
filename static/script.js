// Function to merge two PDFs using pdf-lib
async function mergePDFs(pdf1Bytes, pdf2Bytes) {
  const { PDFDocument } = PDFLib;

  // Create a new PDF document to hold merged content
  const pdfDoc = await PDFDocument.create();

  // Load both PDFs into PDFLib objects
  const pdf1 = await PDFDocument.load(pdf1Bytes);
  const pdf2 = await PDFDocument.load(pdf2Bytes);

  // Copy pages from the first PDF and add to the merged document
  const pages1 = await pdfDoc.copyPages(pdf1, pdf1.getPageIndices());
  pages1.forEach(page => pdfDoc.addPage(page));

  // Copy pages from the second PDF and add to the merged document
  const pages2 = await pdfDoc.copyPages(pdf2, pdf2.getPageIndices());
  pages2.forEach(page => pdfDoc.addPage(page));

  // Save the final merged PDF as a byte array
  return await pdfDoc.save();
}


document.getElementById('pdfForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  // Collect form data and validate
  const university = document.getElementById('txtUniversity').value.trim();
  const department = document.getElementById('txtDepartment').value.trim();
  const subject = document.getElementById('txtSubject').value.trim();
  const submittedTo = document.getElementById('txtSubmittedTo').value.trim();
  const submittedBy = document.getElementById('student-Name').value.trim();
  const rollNo = document.getElementById('roll-No').value.trim();

  if (!submittedBy || !rollNo) {
    alert('Please fill in the required fields.');
    return;
  }

  const statusMessage = document.getElementById('statusMessage');
  statusMessage.textContent = "";


  let strataBlob = null;
  try {
    const response = await fetch('/generate-pdf', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ rollNo: rollNo, studentName: submittedBy })
    });

    if (response.ok) {
      strataBlob = await response.blob();
      // const link = document.createElement('a');
      // link.href = window.URL.createObjectURL(strataBlob);
      // link.download = `${studentName}_strata_experiment_${rollNo}.pdf`;

      // link.click();
      statusMessage.textContent = "PDF generated and downloaded successfully!";
    } else {
      const errorData = await response.json();
      statusMessage.textContent = "Error: " + (errorData.error || "PDF generation failed.");
    }
  } catch (error) {
    console.error("Fetch error:", error);
    statusMessage.textContent = "An error occurred. Please try again.";
  }



  // Create a new PDF using jsPDF
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();


  //Image addition logic
  const imgUrl = 'mdu logo.jpg'; // Replace with your image path or URL

  const image = new Image();
  image.src = 'static/mdu logo.jpg'; // 
  image.onload = function () {
    // Add the image at the specified position
    const imgX = 65; // X position
    const imgY = 40; // Y position (adjusted to center content)
    const imgWidth = 80; // Image width
    const imgHeight = 70; // Image height

    doc.addImage(image, 'JPEG', imgX, imgY, imgWidth, imgHeight); // Add the image

    // Set font to bold for all text
    doc.setFont("Helvetica", "bold");

    // Centered text positioning
    const textX = 105; // Center position for text
    const universityY = imgY + imgHeight + 20; // Position below the image
    // Draw a line after the university name
    doc.setDrawColor(0); // Set the color for the line
    doc.setLineWidth(0.5); // Set line width
    doc.line(30, universityY + 5, 180, universityY + 5); // Line after university name
    const departmentY = universityY + 18; // Spacing below the university name
    const subjectY = departmentY + 23; // Spacing below the department name

    // Add text fields below the image
    doc.setFontSize(24);
    if (university) {
      doc.text(document.getElementById('txtUniversity').value, textX, universityY, { align: 'center' });
    }
    else {
      doc.text('Maharshi Dayanand University,Rohtak', textX, universityY, { align: 'center' });
    }

    doc.setFontSize(20);
    if (department) {
      doc.text(document.getElementById('txtDepartment').value, textX, departmentY, { align: 'center' });
    }
    else {
      doc.text('Department of Mathematics', textX, departmentY, { align: 'center' });
    }


    doc.setFontSize(15);
    doc.text('Practical Of', textX, subjectY-10, { align: 'center' });
    doc.setFontSize(18);
    if (subject) {
      doc.text(document.getElementById('txtSubject').value, textX, subjectY, { align: 'center' });
    }
    else {
      doc.text('Sampling Techniques and Design Of Experiments', textX, subjectY, { align: 'center' });
    }


    // Add submitted to/by details
    const submittedToY = subjectY + 23; // Positioning below subject
    const submittedByY = submittedToY + 10; // Spacing between fields
    const rollNoY = submittedByY + 10; // Spacing for roll number

    doc.setFontSize(16);
    doc.text('Submitted To:', 50, submittedToY);
    doc.text('Submitted By:', 130, submittedToY);
    doc.setFontSize(14);
    if(submittedTo){
      doc.text(`Prof. ${submittedTo}`, 50, submittedByY);
    }
    else{
      doc.text(`Prof. Gulshan Lal Taneja`, 50, submittedByY);
    }
    
    doc.text(document.getElementById('student-Name').value, 130, submittedByY);
    doc.text(`Roll No: ${document.getElementById('roll-No').value}`, 130, rollNoY);
    // Draw a line after the university name
    doc.setDrawColor(0); // Set the color for the line
    doc.setLineWidth(0.5); // Set line width
    doc.line(30, rollNoY + 5, 180, rollNoY + 5); // Line after university name
    // Add footer text
    const courseY = rollNoY + 23; // Position footer below the last entry
    doc.setFontSize(20);
    doc.text('5-Year Integrated M.Sc.(Hons.) Mathematics', textX, courseY, { align: 'center' });
    const footerY = courseY + 10; // Position footer below the last entry
    doc.setFontSize(12);
    doc.text('(8th Sem)', textX, footerY, { align: 'center' });

    // Convert jsPDF output to an ArrayBuffer for merging
    const pdfBytes = doc.output('arraybuffer');

    // 1. Convert strataBlob to ArrayBuffer
    strataBlob.arrayBuffer()
      .then(strataBytes => {
        // 2. First merge: cover page + strata PDF
        return mergePDFs(pdfBytes, strataBytes);
      })
      .then(firstMergeBytes => {
        // 3. Fetch the existing PDF file
        return fetch('static/6-11 experiments.pdf')
          .then(response => {
            if (!response.ok) {
              throw new Error('Failed to fetch existing PDF');
            }
            return response.arrayBuffer();
          })
          .then(existingPdfBytes => {
            // 4. Second merge: (cover+strata) + existing PDF
            return mergePDFs(firstMergeBytes, existingPdfBytes);
          });
      })
      .then(finalPdfBytes => {
        // 5. Create and download the final merged PDF
        const blob = new Blob([finalPdfBytes], { type: 'application/pdf' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `${submittedBy}(${rollNo})_Sampling Techniques.pdf`;
        link.click();

        // Clean up
        URL.revokeObjectURL(link.href);

        statusMessage.textContent = "PDF generated and downloaded successfully!";
      })
      .catch(error => {
        console.error("Error during PDF merging:", error);
        statusMessage.textContent = "Error merging PDFs: " + error.message;
      });
  };


});