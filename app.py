from flask import Flask, request, send_file, render_template, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import random
import math
import os

#Link Of the Project:
#https://sampling-techniques-tables.onrender.com/

app = Flask(__name__, static_folder='static', template_folder='templates')



rollNo_1 = [5401,5411,5421,5431,5441,5451] #500
rollNo_2 = [5402,5412,5422,5432,5442,5452] #550
rollNo_3 = [5403,5413,5423,5433,5443,5453] #600
rollNo_4 = [5404,5414,5424,5434,5444,5454] #650
rollNo_5 = [5405,5415,5425,5435,5445,5455] #700
rollNo_6 = [5406,5416,5426,5436,5446]      #750
rollNo_7 = [5407,5417,5427,5437,5447]      #800
rollNo_8 = [5408,5418,5428,5438,5448]      #850
rollNo_9 = [5409,5419,5429,5439,5449]      #900
rollNo_10 = [5410,5420,5430,5440,5450]     #950 last series of roll numbers

position_map = {
    # For rollNo_1 students
    rollNo_1[0]: {
        0: (470, 645,50), 1: (505, 645,300), 2: (330, 450,50), 3: (330, 470,300), 4: (190, 310,50),
    },
    rollNo_1[1]: {
        0: (530, 655,50), 1: (478, 653,300), 2: (385, 510,50), 3: (330, 455,300), 4: (200, 355,50),
    },
    rollNo_1[2]: {
        0: (530, 655,50), 1: (530, 650,300), 2: (385, 510,50), 3: (295, 505,300), 4: (230, 350,50),
    },
    rollNo_1[3]: {
        0: (505, 645,50), 1: (520, 640,300), 2: (360, 485,50), 3: (375, 500,300), 4: (150, 340,50),
    },
    rollNo_1[4]: {
        0: (430, 640,50), 1: (520, 640,300), 2: (280, 400,50), 3: (380, 495,300), 4: (200, 320,300),
    },
    rollNo_1[5]: {
        0: (430, 640,50), 1: (520, 640,300), 2: (285, 405,50), 3: (380, 500,300), 4: (200, 320,300),
    },

    # For rollNo_2 students
    rollNo_2[0]: {
        0: (420, 650,50), 1: (530, 650,300), 2: (240, 375,50), 3: (380, 495,300), 4: (200, 340,300),
    },
    rollNo_2[1]: {
        0: (520, 650,50), 1: (450, 650,300), 2: (350, 495,50), 3: (240, 425,300), 4: (190, 315,50),
    },
    rollNo_2[2]: {
        0: (530, 650,50), 1: (530, 650,300), 2: (380, 505,50), 3: (310, 505,300), 4: (150, 345,50),
    },
    rollNo_2[3]: {
        0: (470, 650,50), 1: (470, 655,300), 2: (280, 470,50), 3: (320, 445,300), 4: (180, 300,300),
    },
    rollNo_2[4]: {
        0: (530, 650,50), 1: (530, 650,300), 2: (380, 500,50), 3: (270, 495,300), 4: (200, 355,50),
    },
    rollNo_2[5]: {
        0: (500, 640,50), 1: (395, 645,300), 2: (350, 475,50), 3: (240, 360,300), 4: (200, 320,50),
    },
    
    # For rollNo_3 students
    rollNo_3[0]: {
        0: (340, 645,50), 1: (520, 645,300), 2: (190, 310,50), 3: (390, 490,300), 4: (210, 350,300),
    },
    rollNo_3[1]: {
        0: (520, 640,50), 1: (470, 645,300), 2: (360, 485,50), 3: (320, 450,300), 4: (80, 330,50),
    },
    rollNo_3[2]: {
        0: (520, 640,50), 1: (395, 640,300), 2: (380, 495,50), 3: (240, 360,50), 4: (200, 370,300),
    },
    rollNo_3[3]: {
        0: (520, 640,50), 1: (520, 645,300), 2: (380, 495,50), 3: (235, 500,300), 4: (190, 350,50),
    },
    rollNo_3[4]: {
        0: (520, 640,50), 1: (520, 645,300), 2: (265, 490,50), 3: (340, 495,300), 4: (155, 310,300),
    },
    rollNo_3[5]: {
        0: (490, 645,50), 1: (475, 645,300), 2: (300, 460,50), 3: (300, 460,300), 4: (140, 280,50),
    },
    
    # For rollNo_4 students
    rollNo_4[0]: {
        0: (520, 640,50), 1: (520, 645,300), 2: (220, 490,50), 3: (370, 490,300), 4: (150, 340,300),
    },
    rollNo_4[1]: {
        0: (520, 640,50), 1: (520, 645,300), 2: (350, 490,50), 3: (370, 490,300), 4: (20, 340,300),
    },
    rollNo_4[2]: {
        0: (330, 645,50), 1: (515, 645,300), 2: (180, 305,50), 3: (360, 480,300), 4: (195, 340,300),
    },
    rollNo_4[3]: {
        0: (480, 645,50), 1: (520, 645,300), 2: (310, 450,50), 3: (240, 490,300), 4: (120, 280,50),
    },
    rollNo_4[4]: {
        0: (520, 645,50), 1: (520, 645,300), 2: (370, 490,50), 3: (370, 490,300), 4: (10, 350,50),
    },
    rollNo_4[5]: {
        0: (420, 645,50), 1: (490, 645,300), 2: (230, 390,50), 3: (340, 460,300), 4: (120, 280,300),
    },
    
    # For rollNo_5 students
    rollNo_5[0]: {
        0: (410, 645,50), 1: (520, 645,300), 2: (260, 380,50), 3: (330, 490,300), 4: (60, 310,300),
    },
    rollNo_5[1]: {
        0: (490, 645,50), 1: (475, 650,300), 2: (330, 450,50), 3: (275, 455,300), 4: (60, 310,50),
    },
    rollNo_5[2]: {
        0: (530, 655,50), 1: (530, 655,300), 2: (370, 510,50), 3: (350, 510,300), 4: (15, 350,50),
    },
    rollNo_5[3]: {
        0: (310, 645,50), 1: (525, 645,300), 2: (170, 290,50), 3: (340, 500,300), 4: (170, 310,300),
    },
    rollNo_5[4]: {
        0: (310, 645,50), 1: (490, 645,300), 2: (145, 285,50), 3: (350, 470,300), 4: (190, 310,300),
    },
    rollNo_5[5]: {
        0: (360, 645,50), 1: (505, 645,300), 2: (120, 330,50), 3: (350, 470,300), 4: (200, 320,300),
    },
    
    # For rollNo_6 students
    rollNo_6[0]: {
        0: (520, 645,50), 1: (415, 645,300), 2: (150, 490,50), 3: (260, 390,300), 4: (120, 240,300),
    },
    rollNo_6[1]: {
        0: (450, 645,50), 1: (450, 645,300), 2: (245, 420,50), 3: (300, 420,300), 4: (20, 270,300),
    },
    rollNo_6[2]: {
        0: (435, 645,50), 1: (525, 645,300), 2: (100, 400,50), 3: (350, 490,300), 4: (150, 310,300),
    },
    rollNo_6[3]: {
        0: (520, 655,50), 1: (325, 660,300), 2: (370, 490,50), 3: (140, 295,300), 4: (170, 340,50),
    },
    rollNo_6[4]: {
         0: (490, 660,50), 1: (545, 660,300), 2: (340, 460,50), 3: (210, 510,300), 4: (90, 300,50),
    },
    
    # For rollNo_7 students
    rollNo_7[0]: {
        0: (395, 645,50), 1: (325, 645,300), 2: (210,370,50), 3: (180, 300,300), 4: (40, 160,300),
    },
    rollNo_7[1]: {
        0: (520, 645,50), 1: (515, 645,300), 2: (190, 490,50), 3: (205, 485,300), 4: (30, 170,300),
    },
    rollNo_7[2]: {
        0: (540, 660,50), 1: (470, 660,300), 2: (380, 520,50), 3: (255, 475,300), 4: (25, 390,50),
    },
    rollNo_7[3]: {
        0: (500, 655,50), 1: (540, 660,300), 2: (180, 465,50), 3: (390, 515,300), 4: (80, 370,300),
    },
    rollNo_7[4]: {
         0: (470, 660,50), 1: (545, 660,300), 2: (340, 455,50), 3: (310, 520,300), 4: (10, 325,50),
    },
    
    # For rollNo_8 students
    rollNo_8[0]: {
        0: (395, 645,50), 1: (470, 645,300), 2: (210,370,50), 3: (70, 370,300), 4: (60, 180,50),
    },
    rollNo_8[1]: {
        0: (420, 645,50), 1: (313, 645,300), 2: (240, 400,50), 3: (150, 285,300), 4: (60, 200,50),
    },
    rollNo_8[2]: {
        0: (340, 660,50), 1: (467, 660,300), 2: (160, 320,50), 3: (305, 445,300), 4: (80, 280,300),
    },
    rollNo_8[3]: {
        0: (500, 655,50), 1: (360, 660,300), 2: (345, 465,50), 3: (140, 320,300), 4: (80, 325,50),
    },
    rollNo_8[4]: {
         0: (364, 660,50), 1: (545, 660,300), 2: (230, 345,50), 3: (400, 520,300), 4: (40, 375,300),
    },
    
    # For rollNo_9 students
    rollNo_9[0]: {
        0: (385, 645,50), 1: (367, 645,300), 2: (216,340,50), 3: (90, 340,300), 4: (60, 200,50),
    },
    rollNo_9[1]: {
        0: (525, 645,50), 1: (420, 645,300), 2: (170, 485,50), 3: (130, 392,300), 4: (20, 140,50),
    },
    rollNo_9[2]: {
        0: (310, 650,50), 1: (510, 650,300), 2: (165, 285,50), 3: (370, 490,300), 4: (15, 350,300),
    },
    rollNo_9[3]: {
        0: (320, 655,50), 1: (380, 660,300), 2: (130, 285,50), 3: (240, 360,300), 4: (50, 215,300),
    },
    rollNo_9[4]: {
         0: (364, 660,50), 1: (545, 660,300), 2: (230, 345,50), 3: (400, 520,300), 4: (40, 375,300),
    },
    
    # For rollNo_10 students
    rollNo_10[0]: {
        0: (450, 655,50), 1: (540, 655,300), 2: (146,430,50), 3: (285, 527,300), 4: (20, 265,300),
    },
    rollNo_10[1]: {
        0: (410, 655,50), 1: (480, 655,300), 2: (265, 385,50), 3: (120, 460,300), 4: (20, 247,50),
    },
    rollNo_10[2]: {
        0: (330, 660,50), 1: (510, 660,300), 2: (160,300,50), 3: (215, 470,300), 4: (13, 203,300),
    },
    rollNo_10[3]: {
        0: (500, 655,50), 1: (465, 655,300), 2: (145,480,50), 3: (295, 450,300), 4: (15, 275,300),
    },
    rollNo_10[4]: {
        0: (360, 655,50), 1: (540, 655,300), 2: (150,270,300), 3: (290, 514,300), 4: (9, 345,50),
    },
   
}


# yiSum = []
# yi2Sum = []


def draw_table(pdf, data, x, y, col_widths,row_heights=None):
    table = Table(data, colWidths=col_widths, rowHeights=row_heights)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(pdf, 500, 842)
    table.drawOn(pdf, x, y)

def create_pdf(filename, rollNo):
    yiSum = []
    yi2Sum = []
    random.seed(int(rollNo))  # deterministic uniqueness per student

    pdf = canvas.Canvas(filename, pagesize=A4)
    pdf.setTitle("Strata Tables")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 820, "Tabulation and Observations")

    # Determine population size
    rollNo = int(rollNo)
    if rollNo in rollNo_1:
        populationSize = 500
    elif rollNo in rollNo_2:
        populationSize = 550
    elif rollNo in rollNo_3:
        populationSize = 600
    elif rollNo in rollNo_4:
        populationSize = 650
    elif rollNo in rollNo_5:
        populationSize = 700
    elif rollNo in rollNo_6:
        populationSize = 750
    elif rollNo in rollNo_7:
        populationSize = 800
    elif rollNo in rollNo_8:
        populationSize = 850
    elif rollNo in rollNo_9:
        populationSize = 900
    else:
        populationSize = 950

    # Step 1: Randomly divide the population into 5 strata
    cut_points = sorted(random.sample(range(50, populationSize - 50), 4))
    cut_points = [0] + cut_points + [populationSize]

    strata_labels = ["A-E", "F-J", "K-O", "P-T", "U-Z"]
    strata_ranges = {
        strata_labels[i]: (cut_points[i] + 1, cut_points[i + 1])
        for i in range(5)
    }
    
    
    
    
    # Step 2: Compute total sample size (5% of population)
    total_sample = round(0.05 * populationSize)
    min_sample = 4
    max_sample = 16
    
    stratum_sizes = {k: end - start + 1 for k, (start, end) in strata_ranges.items()}
    total_pages = sum(stratum_sizes.values())
    
    
    # Step 3: Distribute sample proportionally
    sample_counts = {}
    for k, size in stratum_sizes.items():
        proportion = (size/total_pages)*total_sample
        count = round(proportion)
        count = max(min_sample, min(count, max_sample)) 
        sample_counts[k] = min(count,size) 

    # Adjust for rounding errors
    adjust = total_sample - sum(sample_counts.values())
    keys = list(sample_counts.keys())
    while adjust != 0:
        k = random.choice(keys)
        if adjust > 0 and sample_counts[k] < min(max_sample,stratum_sizes[k]):
            sample_counts[k] += 1
            adjust -= 1
        elif adjust < 0 and sample_counts[k] > min_sample:
            sample_counts[k] -= 1
            adjust += 1

    # Step 4: Sample pages from each stratum
    strata_pages = {
        k: sorted(random.sample(range(r[0], r[1] + 1), sample_counts[k]))
        for k, r in strata_ranges.items()
    }

    # Step 5: Create strata table
    strata_data = [["Strata", "No. of Pages", "Sample Size", "Pages No."]]
    for k in strata_labels:
        size = stratum_sizes[k]
        count = sample_counts[k]
        pages = ", ".join(map(str, strata_pages[k]))
        strata_data.append([k, str(size), str(count), pages])
    strata_data.append(["", str(populationSize), str(total_sample), ""])

    draw_table(pdf, strata_data, x=30, y=680, col_widths=[50, 65, 65, 365],row_heights=None)

    # Step 6: Detailed stratum-wise tables

    
    tables_data = []
    for idx, (label, pages) in enumerate(strata_pages.items(), start=1):
        table_rows = [["S.No.", "Page No.", f"No. of words(y{idx}i)", f"y{idx}i²"]]
        sum_yi = 0
        sum_yi2 = 0
        for i, page in enumerate(pages): 
            yi = random.randint(10, 50)
            yi2 = yi ** 2
            sum_yi += yi
            sum_yi2 += yi2
            table_rows.append([str(i + 1), str(page), str(yi), str(yi2)])
        yiSum.append(sum_yi)
        yi2Sum.append(sum_yi2)
        
        table_rows.append(["", "Total", str(sum_yi), str(sum_yi2)])
        tables_data.append((f"STRATUM {label}", table_rows))

    # Step 7: Draw each detailed table
    x_left, x_right = 50, 300
    y_position = 450

    
    if(populationSize):
        for i, (title, data) in enumerate(tables_data):
            pdf.setFont("Helvetica-Bold", 10)
            x = x_left if i % 2 == 0 else x_right
            if i % 2 == 0 and i != 0:
                y_position -= 180

            # Look up y positions from the map
            if rollNo in position_map and i in position_map[rollNo]:
                y_position, title_y, x = position_map[rollNo][i]

            pdf.drawString(x, title_y, title)
            draw_table(pdf, data, x, y_position, col_widths=[40, 50, 88, 50],row_heights=None)
    
    pdf.showPage()
    pdf.setFont("Helvetica-Bold",16)
    pdf.drawString(250,820,"Calculations")
    
    
    nySum = 0 
    SD_Sum = 0     
    calcTable=[["Sr. No.","ni","ΣYi","Yi = ΣYi/ni","Ni", "NiYi","(1-fi)/ni","Wi","Si²","((1-fi)/ni)Wi²Si²"],]
    for i,k in enumerate(strata_labels,start=1):
        size = stratum_sizes[k]
        count = sample_counts[k]
        sum_yi = yiSum[i-1]
        sum_yi2 = yi2Sum[i-1]
        yi = round(sum_yi/count,6)
        Fi = round((1-(count/size))/count,6)
        Wi = round(size/int(populationSize),6)
        numerator = (sum_yi2 - (sum_yi ** 2) / count)
        numerator = max(0, numerator)
        sd = round(numerator / (count - 1), 6)
        # sd = round(((sum_yi2) - (sum_yi**2)/count)/(count-1),6)
        SD = round(Fi*(Wi**2)*(sd),6)
        nySum = nySum + yi*size
        SD_Sum = SD_Sum + SD
        calcRow = [str(i), str(count),str(sum_yi),yi,str(size),round(yi*size,6),Fi,Wi,sd,SD]
        calcTable.append(calcRow)
    
    calcTable.append(["Total", "", "", "", "",round(nySum,6), "", "", "", round((SD_Sum),6)])

    draw_table(pdf, calcTable, x = 10,y = 630,col_widths=[40,35,40,70,40,70,50,70,70,85],row_heights=[30,25,25,25,25,25,25])
    
    pdf.save()




@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    rollNo = data.get('rollNo')
    experiment_no = data.get('experimentNo')
    # population_size = data.get('populationSize')
    
    student_name = data.get('studentName')
    if not experiment_no:
        return jsonify({'error': 'Experiment number and roll no. is required'}), 400

    # Create folder if it doesn't exist
    folder_path = os.path.join(os.getcwd(), "generated_pdfs")
    os.makedirs(folder_path, exist_ok=True)

    # Save the PDF in that folder
    filename = f"{student_name}_strata_experiment_{experiment_no}.pdf"
    file_path = os.path.join(folder_path, filename)
    
    # print(f"Generating PDF for {student_name} with roll no {rollNo}")
    create_pdf(file_path,rollNo)

    return send_file(file_path, as_attachment=True)


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)





