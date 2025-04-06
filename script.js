// document.getElementById("downloadForm").addEventListener("submit", async (e) => {
//     e.preventDefault();
  
//     const experimentNumber = document.getElementById("experimentNumber").value;
//     const statusMessage = document.getElementById("statusMessage");
  
//     statusMessage.textContent = "Generating PDF, please wait...";
  
//     try {
//       const response = await fetch("/generate-pdf", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json"
//         },
//         body: JSON.stringify({ experimentNumber })
//       });
  
//       if (!response.ok) {
//         throw new Error("Failed to generate PDF");
//       }
  
//       const blob = await response.blob();
//       const url = window.URL.createObjectURL(blob);
  
//       const a = document.createElement("a");
//       a.href = url;
//       a.download = `Experiment_${experimentNumber}_Strata.pdf`;
//       document.body.appendChild(a);
//       a.click();
//       a.remove();
  
//       statusMessage.textContent = "PDF generated successfully!";
//     } catch (err) {
//       console.error(err);
//       statusMessage.textContent = "Error generating PDF.";
//     }
//   });
  