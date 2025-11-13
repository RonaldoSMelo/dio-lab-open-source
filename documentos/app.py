#!/usr/bin/env python3
"""
Aplicação Flask para PDF Merger com interface web
Permite upload de arquivos e reordenação via drag-and-drop
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import tempfile
import shutil
from pdf_merger import PDFMerger

app = Flask(__name__)
app.secret_key = 'pdf_merger_secret_key_2025'

# Configurações
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif', 'gif', 'pdf'
}

# Criar diretórios se não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_info(filepath):
    """Obtém informações do arquivo"""
    file_path = Path(filepath)
    stat = file_path.stat()
    
    return {
        'name': file_path.name,
        'size': stat.st_size,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'extension': file_path.suffix.lower(),
        'type': 'image' if file_path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'} else 'pdf'
    }

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Upload de arquivos"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        files = request.files.getlist('files')
        uploaded_files = []
        
        for file in files:
            if file.filename == '':
                continue
                
            if file and allowed_file(file.filename):
                # Salvar arquivo
                filename = secure_filename(file.filename)
                
                # Evitar conflitos de nome
                counter = 1
                original_name = filename
                while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    name, ext = os.path.splitext(original_name)
                    filename = f"{name}_{counter}{ext}"
                    counter += 1
                
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Obter informações do arquivo
                file_info = get_file_info(filepath)
                file_info['id'] = filename  # ID único para o front-end
                file_info['filepath'] = filepath
                
                uploaded_files.append(file_info)
            else:
                return jsonify({'error': f'Arquivo não permitido: {file.filename}'}), 400
        
        return jsonify({
            'success': True,
            'files': uploaded_files,
            'message': f'{len(uploaded_files)} arquivo(s) enviado(s) com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro no upload: {str(e)}'}), 500

@app.route('/process', methods=['POST'])
def process_files():
    """Processar arquivos e gerar PDF"""
    try:
        data = request.get_json()
        
        if not data or 'files' not in data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        files_order = data['files']  # Lista com ordem dos arquivos
        output_name = data.get('output_name', 'documento_final')
        
        if not files_order:
            return jsonify({'error': 'Nenhum arquivo para processar'}), 400
        
        # Verificar se todos os arquivos existem
        file_paths = []
        for file_id in files_order:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
            if not os.path.exists(filepath):
                return jsonify({'error': f'Arquivo não encontrado: {file_id}. Faça upload novamente.'}), 404
            file_paths.append(filepath)
        
        # Gerar PDF
        merger = PDFMerger()
        output_filename = f"{secure_filename(output_name)}.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        if merger.merge_files_to_pdf(file_paths, output_path):
            return jsonify({
                'success': True,
                'output_file': output_filename,
                'message': 'PDF gerado com sucesso',
                'download_url': f'/download/{output_filename}'
            })
        else:
            return jsonify({'error': 'Erro ao gerar PDF. Verifique os arquivos.'}), 500
            
    except Exception as e:
        print(f"Erro no processamento: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download do arquivo gerado"""
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'Arquivo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro no download: {str(e)}'}), 500

@app.route('/clear', methods=['POST'])
def clear_files():
    """Limpar arquivos temporários"""
    try:
        # Limpar pasta de uploads
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        return jsonify({'success': True, 'message': 'Arquivos limpos com sucesso'})
        
    except Exception as e:
        return jsonify({'error': f'Erro ao limpar arquivos: {str(e)}'}), 500

@app.route('/files')
def list_files():
    """Listar arquivos no diretório de upload"""
    try:
        files = []
        upload_dir = app.config['UPLOAD_FOLDER']
        
        for filename in os.listdir(upload_dir):
            filepath = os.path.join(upload_dir, filename)
            if os.path.isfile(filepath) and allowed_file(filename):
                file_info = get_file_info(filepath)
                file_info['id'] = filename
                files.append(file_info)
        
        return jsonify({'files': files})
        
    except Exception as e:
        return jsonify({'error': f'Erro ao listar arquivos: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Erro de arquivo muito grande"""
    return jsonify({'error': 'Arquivo muito grande. Tamanho máximo: 50MB'}), 413

@app.errorhandler(500)
def internal_error(e):
    """Erro interno do servidor"""
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando PDF da Cintia Merge Web Interface...")
    print(f"📁 Pasta de uploads: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"📁 Pasta de saída: {os.path.abspath(OUTPUT_FOLDER)}")
    print("🌐 Acesse: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
