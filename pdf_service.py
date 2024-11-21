from river_registry import RiverRegistry
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from datetime import datetime

REPORTS_DIR = "reports"
GRAPH_FILE = os.path.join(REPORTS_DIR, "variation_graphs.png")

def create_pdf_report(river_level_list: list[RiverRegistry], var_1h: float, var_6h: float, var_24h: float, flood_alert: bool):
    create_report_dir_if_not_exists()
    
    create_variation_graphs(river_level_list)
    
    pdf_filename = generate_pdf_filename()
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    draw_report_header(c)
    draw_variations(c, var_1h, var_6h, var_24h)
    draw_flood_status(c, flood_alert)
    draw_graph(c)
    
    finalize_report(c, pdf_filename)

def create_report_dir_if_not_exists():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

def generate_pdf_filename() -> str:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(REPORTS_DIR, f"guaiba_river_report_{now}.pdf")

def draw_report_header(c: canvas.Canvas):
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Relatório de Nível do Rio Guaíba - Porto Alegre, RS")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

def draw_variations(c: canvas.Canvas, var_1h: float, var_6h: float, var_24h: float):
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Variação 1h: {var_1h} metros")
    c.drawString(50, 680, f"Variação 6h: {var_6h} metros")
    c.drawString(50, 660, f"Variação 24h: {var_24h} metros")

def draw_flood_status(c: canvas.Canvas, flood_alert: bool):
    c.setFont("Helvetica-Bold", 14)
    if flood_alert:
        c.setFillColorRGB(1, 0, 0) 
        c.drawString(50, 620, "⚠️ ALERTA DE INUNDAÇÃO!")
    else:
        c.setFillColorRGB(0, 0.5, 0)
        c.drawString(50, 620, "✓ Níveis normais")

def draw_graph(c: canvas.Canvas):
    c.drawImage(GRAPH_FILE, 50, 200, width=500, height=400)

def finalize_report(c: canvas.Canvas, pdf_filename: str):
    c.save()
    os.remove(GRAPH_FILE)
    print(f"Relatório gerado: {pdf_filename}")

def create_variation_graphs(river_level_list: list[RiverRegistry]):
    hourly_data = get_hourly_data(river_level_list)
    plot_graph(hourly_data)

def get_hourly_data(river_level_list: list[RiverRegistry]) -> list[RiverRegistry]:
    hourly_data = []
    current_hour = None
    
    for reg in river_level_list:
        hour = reg.date.replace(minute=0, second=0, microsecond=0)
        if hour != current_hour:
            hourly_data.append(reg)
            current_hour = hour
            
    return hourly_data

def plot_graph(hourly_data: list[RiverRegistry]):
    plt.figure(figsize=(10, 8))
    
    times = [reg.date.strftime("%d/%m/%Y - %H:00") for reg in hourly_data]
    levels = [reg.river_level for reg in hourly_data]
    
    plt.plot(times, levels, marker='o')
    plt.title("Variação do Nível do Rio Guaíba - 24h")
    plt.xlabel("Data/Hora") 
    plt.ylabel("Nível (metros)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(GRAPH_FILE)
    plt.close()