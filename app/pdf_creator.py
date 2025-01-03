##############################################################################################################


from flask import Flask, request, send_file, jsonify
from docxtpl import DocxTemplate
from openpyxl import Workbook
import subprocess
import os
from dotenv import load_dotenv
import base64

app = Flask(__name__)

@app.route('/generate_file', methods=['POST'])
def generate_file():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    template_data = base64.b64decode(data.get('template', ''))
    output_format = data.get('output_format', '').lower()
    
    if not template_data or not output_format:
        return jsonify({'error': 'Missing template or output_format'}), 400
    
    template_path = os.path.join(os.getenv('UPLOAD_FOLDER'), 'template_file')
    with open(template_path, 'wb') as f:
        f.write(template_data)
    
    if output_format == 'pdf':
        generate_pdf(template_path)
        output_file = os.path.join(os.getenv('OUTPUT_FOLDER'), 'result.pdf')
    elif output_format == 'excel':
        generate_excel(template_path, data.get('rendering_data', {}))
        output_file = os.path.join(os.getenv('OUTPUT_FOLDER'), 'result.xlsx')
    elif output_format == 'word':
        generate_word(template_path, data.get('rendering_data', {}))
        output_file = os.path.join(os.getenv('OUTPUT_FOLDER'), 'result.docx')
    else:
        return jsonify({'error': 'Unsupported output_format'}), 400
    
    return send_file(output_file, as_attachment=True)

def generate_word(template_path, rendering_data):
    template = DocxTemplate(template_path)
    context = rendering_data
    
    # Render the template with the data
    template.render(context)
    output_path = os.path.join(os.getenv('OUTPUT_FOLDER'), 'result.docx')
    template.save(output_path)
    
def generate_excel(template_path, rendering_data):
    workbook = Workbook()
    sheet = workbook.active
    
    # Assign rendering_data to cells in the first column
    for idx, (key, value) in enumerate(rendering_data.items(), start=1):
        sheet.cell(row=idx, column=1, value=key)
        sheet.cell(row=idx, column=2, value=value)
    
    output_path = os.path.join(os.getenv('OUTPUT_FOLDER'), 'result.xlsx')
    workbook.save(output_path)

def generate_pdf(template_path):
    command = ['libreoffice', '--convert-to', 'pdf', '--headless', '--writer', '--outdir', os.getenv('OUTPUT_FOLDER'), template_path]
    subprocess.run(command, check=True)

if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=5000)




