from datetime import date
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether

ROOT = Path(__name__).resolve().parent
OUTPUT = ROOT / "Project_Report.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=28, alignment=TA_CENTER, textColor=colors.HexColor("#183B56")))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=11, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#44546A")))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#1F4E78"), spaceBefore=12, spaceAfter=8))
styles.add(ParagraphStyle(name="SubSection", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=colors.HexColor("#2F5597"), spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyCustom", parent=styles["BodyText"], fontSize=9.5, leading=13.5, alignment=4, spaceAfter=7))
styles.add(ParagraphStyle(name="Caption", parent=styles["Normal"], fontSize=8.5, alignment=TA_CENTER, textColor=colors.HexColor("#44546A"), leading=11))

def P(text, style="BodyCustom"):
    return Paragraph(text, styles[style])

def table(data, widths=None, header=True):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#B4C7E7")), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("FONTNAME", (0,0), (-1,-1), "Helvetica"), ("FONTSIZE", (0,0), (-1,-1), 8.2), ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5), ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4)]
    if header:
        cmds += [("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1F4E78")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")]
    t.setStyle(TableStyle(cmds))
    return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#A6A6A6"))
    canvas.line(doc.leftMargin, 0.55*inch, A4[0]-doc.rightMargin, 0.55*inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(doc.leftMargin, 0.35*inch, "Mini-Courier Planner — DAA Capstone")
    canvas.drawRightString(A4[0]-doc.rightMargin, 0.35*inch, str(doc.page))
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=0.65*inch, leftMargin=0.65*inch, topMargin=0.65*inch, bottomMargin=0.72*inch, title="Mini-Courier Planner DAA Capstone Report", author="Keshav")
story = []

story += [Spacer(1, 0.75*inch), P("K.R. MANGALAM UNIVERSITY", "CoverSub"), Spacer(1, 0.12*inch), P("MINI-COURIER PLANNER", "CoverTitle"), Spacer(1, 0.12*inch), P("Parcel prioritization, packing and route planning using Merge Sort, Dynamic Programming, Dijkstra and Nearest-Neighbor TSP", "CoverSub"), Spacer(1, 0.45*inch)]
cover_table = table([
    ["Programme / Course", "B.Tech CSE Core A — Design & Analysis of Algorithms (ETCCDA302)"],
    ["Submitted by", "Keshav"],
    ["Roll No.", "2501010070"],
    ["Submission date", "25 November 2026"],
], widths=[1.55*inch, 4.75*inch], header=False)
story += [cover_table, Spacer(1, 0.65*inch), P("CAPSTONE PROJECT REPORT", "CoverSub"), PageBreak()]

story += [P("Contents", "Section")]
contents = [
("1", "Introduction"), ("2", "Problem Statement and Objectives"), ("3", "System Design"),
("4", "Implementation and Algorithms"), ("5", "Experimental Results"), ("6", "Performance Analysis"),
("7", "Correctness and Limitations"), ("8", "Conclusion and Future Scope"), ("9", "Screenshots and References")]
story += [table([[n, title] for n,title in contents], widths=[0.55*inch, 5.75*inch], header=False), PageBreak()]

story += [P("1. Introduction", "Section"), P("A courier system must decide which parcels are urgent, which parcels fit into the van, and in what order deliveries should be made. The Mini-Courier Planner integrates sorting, packing, shortest-path search, and route construction into one Python application. The work follows a modular pipeline: the output of one stage becomes the input of the next."), P("The project implements Merge Sort for deadline-based prioritization, 0/1 Knapsack with Dynamic Programming for parcel selection, Dijkstra's algorithm for shortest road distances, and the Nearest-Neighbor heuristic for a Travelling Salesman Problem (TSP) route.")]

story += [P("2. Problem Statement and Objectives", "Section"), P("<b>Problem statement:</b> Given a set of parcels and a road graph, generate a prioritized parcel list, an optimized packing plan under a weight limit, and an ordered delivery route."), P("<b>Objectives:</b>"), P("• Sort parcels by smaller deadline; break ties using higher value.<br/>• Select the maximum-value set of whole parcels that fits within 15 kg.<br/>• Calculate shortest distances between the depot and delivery locations.<br/>• Build a closed route beginning and ending at the depot.<br/>• Verify correctness and compare performance across input sizes."), P("Assumptions: roads are undirected and have non-negative distances; each parcel is carried whole or left behind; one van trip has a capacity of 15 kg.")]

story += [P("3. System Design", "Section"), P("The system is organized as a four-stage pipeline: Parcels → Merge Sort → Knapsack → Dijkstra → Nearest-Neighbor TSP."), P("Modules", "SubSection")]
module_data = [["File", "Responsibility"],["data.py","Defines Parcel objects and sample graph data"],["sorting.py","Merge Sort and deadline/value comparison"],["knapsack.py","Two-dimensional DP and backtracking"],["graph.py","Dijkstra, path reconstruction and distance table"],["route.py","Delivery-point extraction and Nearest-Neighbor route"],["main.py","Runs the complete pipeline and expands the route"],["performance.py","Benchmarks stages and verifies correctness"]]
story += [table(module_data, widths=[1.35*inch, 4.95*inch]), P("Data Model", "SubSection")]
parcels = [["ID","Weight","Value","Deadline","Location"],["P1","5","60","2","1"],["P2","3","40","1","2"],["P3","4","50","3","3"],["P4","6","70","2","4"],["P5","2","30","4","5"],["P6","7","80","5","3"]]
story += [table(parcels, widths=[0.9*inch,1.15*inch,1.15*inch,1.15*inch,1.15*inch]), Spacer(1,7), P("Table 1: Sample parcel dataset")]
roads = [["Road","0–1","0–2","1–2","1–3","2–3","2–4","3–4","3–5","4–5"],["Distance","4","2","1","5","8","10","2","6","3"]]
story += [table(roads, widths=[0.7*inch]+[0.62*inch]*9), Spacer(1,7), P("Table 2: Undirected sample roads", "Caption")]

story += [P("4. Implementation and Algorithms", "Section")]
story += [P("4.1 Merge Sort", "SubSection"), P("Merge Sort recursively divides the parcel list and merges sorted halves. The comparison prioritizes the smallest deadline; for equal deadlines, it chooses the larger value. The algorithm is stable and takes O(n log n) time and O(n) auxiliary space."), P("Result: P2 → P4 → P1 → P3 → P5 → P6.")]
story += [P("4.2 0/1 Knapsack with Dynamic Programming", "SubSection"), P("A 2D table <b>table[i][w]</b> stores the maximum value achievable using the first i parcels under weight limit w. For every parcel, the program compares skipping it with taking it when it fits. Backtracking identifies the selected items. Time and space complexity are O(n × W), where W is the capacity. Backtracking adds O(n) work."), P("Result: P2, P4, P3 and P5 are selected. The total weight is 3 + 6 + 4 + 2 = 15 kg, and the total value is 40 + 70 + 50 + 30 = 190.")]
story += [P("4.3 Dijkstra's Algorithm", "SubSection"), P("Dijkstra initializes all distances as infinity except the source node, uses a min-heap to retrieve the nearest unvisited node, and performs edge relaxation. A previous-node dictionary enables reconstruction of actual road paths. The algorithm takes O((V + E) log V) time per source under the heap implementation and requires non-negative edge weights."), P("Selected delivery points: 2, 4, 3 and 5. Distances from depot 0 are 2, 10, 8 and 13 respectively.")]
story += [P("4.4 Nearest-Neighbor TSP", "SubSection"), P("The route starts at the depot and repeatedly chooses the nearest unvisited delivery point. It then returns to the depot. This greedy method takes O(k²) time for k delivery points but provides an approximation rather than an exact TSP solution."), P("The complete route is <b>0 → 2 → 3 → 4 → 5 → 0</b>. Each leg costs 2, 6, 2, 3 and 13, giving a total route length of 26."), P("The function build_full_path() expands shortest-distance legs into real road nodes using Dijkstra: <b>[0, 2, 1, 3, 4, 5, 4, 3, 1, 2, 0]</b>.")]

story += [P("5. Experimental Results", "Section")]
final_results = [["Stage","Final Result"],["Sorted order","P2, P4, P1, P3, P5, P6"],["Packing","P2, P4, P3, P5"],["Weight / Value","15 kg / 190"],["Delivery points","[2, 4, 3, 5]"],["TSP route","0 → 2 → 3 → 4 → 5 → 0"],["Route length","26"],["Actual road path","0, 2, 1, 3, 4, 5, 4, 3, 1, 2, 0"]]
story += [table(final_results, widths=[1.55*inch,4.75*inch])]
story += [P("Why P6 was not selected: P6 has the largest individual value (80), but only 11.4 value per kg. P2, P4, P3 and P5 form the maximum combination and exactly fill the 15 kg capacity."), P("Why the route returns to the depot: the van starts and ends at the depot, so the tour is closed."), P("Why the TSP result is approximate: a nearest neighbor can make a locally optimal choice that produces a longer final leg, in this case 5 → 0 costing 13.")]

story += [P("6. Performance Analysis", "Section"), P("The performance test uses time.perf_counter() and takes the fastest of three runs. It compares the implemented merge sort with Python's built-in sort and two knapsack implementations. Dijkstra and the route heuristics are also measured."), P("Recorded benchmark", "SubSection")]
bench = [["Parcels","Merge Sort","Built-in Sort","Knapsack 2D","Knapsack 1D","Dijkstra","TSP","Correct"],["10","0.009","0.001","0.04","0.01","0.13","0.003","Yes"],["50","0.049","0.007","0.53","0.24","0.88","0.010","Yes"],["100","0.101","0.014","2.08","0.75","4.35","0.041","Yes"],["200","0.216","0.027","8.55","3.25","18.04","0.133","Yes"],["400","0.466","0.060","34.83","13.22","83.53","0.993","Yes"]]
story += [table(bench, widths=[0.62*inch,0.75*inch,0.82*inch,0.82*inch,0.82*inch,0.72*inch,0.58*inch,0.55*inch]), Spacer(1,7), P("Table 3: Stage runtimes in milliseconds", "Caption")]
for image_name, caption in [("runtime_chart.png","Figure 1: Runtime trend for each stage"),("comparison_chart.png","Figure 2: Comparison of stages at 400 parcels")]:
    p = ROOT / image_name
    if p.exists():
        story += [Spacer(1,10), Image(str(p), width=6.3*inch, height=3.15*inch), P(caption, "Caption")]

story += [P("7. Correctness and Limitations", "Section")]
checks = [["Check","Result"],["Merge sort against Python sorted()","Passed for test datasets"],["Knapsack against brute force","5/5 random trials passed"],["Van capacity","Never exceeded 15 kg"],["Route coverage","Starts and ends at depot; visits each delivery point once"],["Dijkstra weights","Passed on a non-negative, undirected sample graph"]]
story += [table(checks, widths=[2.25*inch,4.05*inch]), P("Limitations: knapsack maximizes value rather than deadline urgency, so an urgent parcel may be excluded. Nearest-Neighbor does not guarantee the shortest TSP tour. The output is based on a fixed sample dataset unless the data module is modified.")]

story += [P("8. Conclusion and Future Scope", "Section"), P("The project successfully demonstrates the integration of four core DAA techniques in a practical parcel-planning scenario. Merge Sort provides a predictable ordering, DP produces an exact packing choice, Dijkstra calculates reliable shortest roads, and Nearest-Neighbor provides a practical route approximation."), P("Future improvements include 1D knapsack storage for lower memory use, deadline-aware parcel priorities, exact TSP search for small stop sets, route optimization using 2-opt, database input, and a graphical or web interface.")]

story += [P("9. Screenshots and References", "Section"), P("Project screenshots are stored in the screenshots/ folder, including data, sorting, knapsack, Dijkstra, route, full program, and performance outputs."), P("References", "SubSection")]
refs = ["Cormen, Leiserson, Rivest & Stein, Introduction to Algorithms.", "Python Software Foundation, Python 3 Documentation.", "Project README and source code in the submitted folder."]
story += [P("• " + r) for r in refs]

story += [PageBreak(), P("Declaration", "Section"), P("I hereby declare that this project report describes the Mini-Courier Planner implementation submitted for the Design & Analysis of Algorithms capstone assignment."), Spacer(1,0.25*inch), P("Name: Keshav"), P("Roll No.: 2501010070"), P("Date: 25 November 2026")]

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
