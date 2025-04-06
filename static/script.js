document.getElementById('downloadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const experimentNumber = document.getElementById('experimentNumber').value;
    const studentName = document.getElementById('studentName').value;
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = "";

    if (!experimentNumber || !studentName)  {
      alert("Please enter an experiment number and your name.");
      return;
    }

    try {
      const response = await fetch('/generate-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ experimentNo: experimentNumber, studentName: studentName })
      });

      if (response.ok) {
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = `${studentName}_strata_experiment_${experimentNumber}.pdf`;
        link.click();
        statusMessage.textContent = "PDF generated and downloaded successfully!";
      } else {
        const errorData = await response.json();
        statusMessage.textContent = "Error: " + (errorData.error || "PDF generation failed.");
      }
    } catch (error) {
      console.error("Fetch error:", error);
      statusMessage.textContent = "An error occurred. Please try again.";
    }
  });