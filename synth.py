from PIL import Image, ImageDraw, ImageFont
from faker import Faker
import json
import os

# ================ INPUTS ================
# ========== CONFIG ==========
TEMPLATE_PATH = "templates/tor.jpg"       # Your template image
COORDS_PATH = "coords/tor.json"            # JSON with field boxes
OUTPUT_DIR = "images/output/tor"                # Output folder

NUM_SYNTHETIC = 10                       # Number of synthetic images
FONT_PATH = "C:/Windows/Fonts/arial.ttf" # Adjust font path

os.makedirs(OUTPUT_DIR, exist_ok=True)
fake = Faker()

# Repeating nouns
name1 = fake.name()
name2 = fake.name()

# Paragraph Fields
minutes = [
    "The meeting was called to order at 9:05 AM by the Chairperson. The minutes of the previous session were read and approved without revisions. Mr. Dela Cruz presented the quarterly financial report, highlighting a 12% increase in operational costs. Members discussed potential budget adjustments to address the deficit. Ms. Ramos proposed a review of procurement policies to ensure compliance with updated regulations. The committee agreed to form a task group to handle this recommendation. The meeting adjourned at 10:30 AM with the next session scheduled for October 12, 2025.",

    "At 2:00 PM, the Planning Committee convened to discuss the progress of ongoing campus infrastructure projects. Engr. Bautista reported delays due to weather conditions affecting construction timelines. Dr. Gomez emphasized the need for updated documentation before the next accreditation audit. The members decided to extend the submission deadline for project reports by two weeks. The budget allocation for maintenance works was also reviewed and approved. Before adjournment, Mr. Tan volunteered to oversee procurement follow-ups. The meeting was adjourned at 3:20 PM.",

    "The meeting commenced at 8:45 AM under the leadership of the Dean. Attendance was verified, and a quorum was declared present. The first agenda item focused on faculty workload adjustments for the upcoming semester. Discussions centered on balancing class hours with research commitments. Dr. Santos recommended revising the workload matrix to ensure fairness among departments. The motion was seconded and approved unanimously. The meeting ended at 10:00 AM after setting the next session for November 4, 2025.",

    "The Research Council meeting began promptly at 1:15 PM with Dr. Cruz presiding. The committee reviewed ongoing funded projects and their respective timelines. Several researchers raised concerns about delays in budget disbursement. The council agreed to submit a formal request for expedited release of funds to the Finance Office. A proposal for a research colloquium in March 2026 was also discussed and endorsed. Dr. Reyes volunteered to lead the organizing committee. The meeting concluded at 2:45 PM.",

    "The Student Affairs Committee meeting was called to order at 10:00 AM. The minutes of the previous meeting were approved after minor corrections. Ms. Lopez presented the results of the student satisfaction survey conducted in September. The members deliberated on measures to improve counseling services and extracurricular engagement. Mr. Hernandez proposed conducting leadership workshops for student organization officers. The proposal was supported and will be implemented next semester. The meeting adjourned at 11:40 AM.",

    "At 3:00 PM, the Administrative Council gathered to discuss updates on personnel and logistics. The HR Department presented the list of employees due for performance evaluation this quarter. Mr. Ramos raised the issue of delays in supply deliveries for office equipment. The council agreed to review the current supplier contract and explore alternative vendors. A separate discussion on the implementation of flexible work arrangements followed. The group resolved to pilot the setup for two months before full rollout. The meeting was adjourned at 4:35 PM.",

    "The meeting opened at 9:30 AM with the Chair acknowledging the presence of all committee members. The agenda focused on finalizing preparations for the upcoming academic audit. Reports from various departments were presented and reviewed. Several discrepancies in data submission were noted and addressed. Dr. Bautista emphasized adherence to documentation standards required by the accrediting body. It was agreed that all departments must finalize their files by the end of the week. The meeting ended at 11:10 AM.",

    "The Curriculum Review Committee convened at 1:00 PM to deliberate on proposed revisions to the Bachelor of Science programs. Dr. Navarro presented the updated course outlines incorporating new CHED standards. Faculty members discussed the integration of digital literacy modules into core subjects. Concerns were raised regarding the availability of trained instructors for new electives. The Dean assured that training programs will be conducted prior to implementation. The revisions were approved unanimously. The meeting adjourned at 2:25 PM.",

    "The Environmental Committee meeting started at 8:15 AM with Mr. Velasco presiding. The primary topic was the implementation of waste segregation policies across all university departments. Ms. Rivera reported challenges in student compliance and proposed an awareness campaign. The committee discussed the use of signage and color-coded bins to improve participation. A budget of ₱25,000 was approved for campaign materials and logistics. Mr. Cruz volunteered to lead the monitoring team. The meeting was adjourned at 9:40 AM.",

    "The Board of Trustees meeting was held at 10:30 AM to finalize the institution’s five-year strategic plan. Dr. Mendoza presented the proposed objectives focusing on research, community extension, and digital transformation. Board members commended the alignment of goals with the university’s mission and vision. Several recommendations were made regarding funding allocations and key performance indicators. After deliberation, the strategic plan was approved with minor revisions. The Secretary was tasked to circulate the final copy for signature. The meeting adjourned at 12:15 PM."
]
minutes_prog = 2

# Load coordinates
with open(COORDS_PATH, "r") as f:
    coords = json.load(f)

# ========== SYNTHETIC DATA GENERATOR ==========
def generate_field_value(field_name):
    """Generate a fake value for a given field."""
    if field_name == "name1":
        return name1
    elif field_name == "region":
        return str(fake.random_int(min=1, max=13))
    elif field_name == "name":
        return fake.name()
    elif field_name == "minutes":
        global minutes_prog
        minutes_prog += 1
        return minutes[minutes_prog - 1]
    elif field_name == "num":
        return str(fake.random_int(min=100000, max=999999))
    elif field_name == "city":
        return fake.city()
    elif field_name == "position":
        return fake.job()
    elif field_name == "place":
        return fake.address().replace("\n", ", ")
    elif field_name == "date":
        return fake.date()
    elif field_name == "school":
        base = fake.company()
        # Randomly choose a type to make it look like an educational institution
        edu_type = fake.random_element(elements=("University", "College", "Institute", "Academy", "School"))
        text = f"{base} {edu_type}"
        return text
    elif field_name == "year":
        return fake.year()
    else:
        return "N/A"

# =================== END OF INPUTS ===================

import textwrap

# ========== MAIN LOOP ==========
for i in range(NUM_SYNTHETIC):
    # Open template
    img = Image.open(TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)

    for item in coords:
        field_name = item["field"]
        x, y, w, h = item["x"], item["y"], item["w"], item["h"]

        # 1️⃣ Fill box with white
        draw.rectangle([x, y, x + w, y + h], fill="white")

        # 2️⃣ Generate new fake text for this field
        text = generate_field_value(field_name)

        # 3️⃣ Start with a reasonable font size (box height)
        font_size = h
        font = ImageFont.truetype(FONT_PATH, font_size)

        # 4️⃣ Function to wrap text within width
        def wrap_text(text, font, max_width):
            words = text.split()
            lines = []
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                if draw.textlength(test_line, font=font) <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word
            if line:
                lines.append(line)
            return lines

        # 5️⃣ Auto-shrink font until wrapped text fits box height
        while font_size > 5:
            font = ImageFont.truetype(FONT_PATH, font_size)
            lines = wrap_text(text, font, w)
            total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)

            if total_height <= h:
                break
            font_size -= 1

        # 6️⃣ Center wrapped text vertically
        current_y = y + (h - total_height) // 2

        for line in lines:
            text_width = draw.textlength(line, font=font)
            text_x = x + (w - text_width) // 2
            draw.text((text_x, current_y), line, fill="black", font=font)
            current_y += font.getbbox(line)[3] - font.getbbox(line)[1]

    # Save output
    out_path = os.path.join(OUTPUT_DIR, f"tor_synth_{i+1}.png")
    img.save(out_path)
    print(f"✅ Generated: {out_path}")