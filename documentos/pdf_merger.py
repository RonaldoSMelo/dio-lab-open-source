#!/usr/bin/env python3
"""
Script para juntar imagens e arquivos PDF em um único arquivo PDF
com opção de ordenação dos arquivos.

Suporta formatos de imagem: JPG, JPEG, PNG, BMP, TIFF, GIF
Suporta arquivos PDF existentes

Autor: Assistente IA
Data: 2025-09-21
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple
import argparse
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import img2pdf

class PDFMerger:
    def __init__(self):
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
        self.supported_pdf_format = '.pdf'
        
    def get_files_from_directory(self, directory: str) -> List[str]:
        """
        Obtém todos os arquivos suportados de um diretório.
        """
        directory_path = Path(directory)
        files = []
        
        for file_path in directory_path.iterdir():
            if file_path.is_file():
                extension = file_path.suffix.lower()
                if extension in self.supported_image_formats or extension == self.supported_pdf_format:
                    files.append(str(file_path))
        
        return files
    
    def sort_files(self, files: List[str], sort_method: str = 'name') -> List[str]:
        """
        Ordena os arquivos de acordo com o método especificado.
        
        Args:
            files: Lista de caminhos de arquivos
            sort_method: 'name' (alfabético), 'date' (data de modificação), 'size' (tamanho)
        
        Returns:
            Lista de arquivos ordenados
        """
        if sort_method == 'name':
            return sorted(files, key=lambda x: Path(x).name.lower())
        elif sort_method == 'date':
            return sorted(files, key=lambda x: Path(x).stat().st_mtime)
        elif sort_method == 'size':
            return sorted(files, key=lambda x: Path(x).stat().st_size)
        else:
            return files
    
    def custom_sort_files(self, files: List[str]) -> List[str]:
        """
        Permite ao usuário ordenar os arquivos manualmente.
        """
        print("\nArquivos encontrados:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {Path(file).name}")
        
        print("\nEscolha a ordem dos arquivos (digite os números separados por vírgula):")
        print("Exemplo: 3,1,4,2 para reordenar os arquivos")
        
        try:
            order_input = input("Nova ordem (ou Enter para manter ordem atual): ").strip()
            if not order_input:
                return files
            
            indices = [int(x.strip()) - 1 for x in order_input.split(',')]
            
            # Verificar se todos os índices são válidos
            if all(0 <= i < len(files) for i in indices) and len(indices) == len(files):
                return [files[i] for i in indices]
            else:
                print("Ordem inválida. Mantendo ordem original.")
                return files
                
        except (ValueError, IndexError):
            print("Entrada inválida. Mantendo ordem original.")
            return files
    
    def convert_image_to_pdf_bytes(self, image_path: str) -> bytes:
        """
        Converte uma imagem para bytes PDF.
        """
        try:
            # Abrir e processar a imagem
            with Image.open(image_path) as img:
                # Converter para RGB se necessário (para JPEGs)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Usar img2pdf para conversão mais eficiente
                pdf_bytes = img2pdf.convert(image_path)
                return pdf_bytes
                
        except Exception as e:
            print(f"Erro ao converter imagem {image_path}: {e}")
            return None
    
    def merge_files_to_pdf(self, files: List[str], output_path: str) -> bool:
        """
        Junta todos os arquivos (imagens e PDFs) em um único PDF.
        """
        writer = PdfWriter()
        
        try:
            for file_path in files:
                file_extension = Path(file_path).suffix.lower()
                
                print(f"Processando: {Path(file_path).name}")
                
                if file_extension in self.supported_image_formats:
                    # Converter imagem para PDF
                    pdf_bytes = self.convert_image_to_pdf_bytes(file_path)
                    if pdf_bytes:
                        # Criar um leitor PDF temporário dos bytes da imagem
                        from io import BytesIO
                        pdf_reader = PdfReader(BytesIO(pdf_bytes))
                        for page in pdf_reader.pages:
                            writer.add_page(page)
                
                elif file_extension == self.supported_pdf_format:
                    # Adicionar páginas do PDF existente
                    pdf_reader = PdfReader(file_path)
                    for page in pdf_reader.pages:
                        writer.add_page(page)
            
            # Salvar o PDF final
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar PDF: {e}")
            return False
    
    def interactive_mode(self):
        """
        Modo interativo para seleção de arquivos e configurações.
        """
        print("=== PDF Merger - Modo Interativo ===\n")
        
        # Escolher fonte dos arquivos
        print("Como você quer selecionar os arquivos?")
        print("1. Pasta específica")
        print("2. Arquivos individuais")
        
        choice = input("Escolha (1 ou 2): ").strip()
        
        files = []
        
        if choice == '1':
            directory = input("Digite o caminho da pasta: ").strip()
            if os.path.exists(directory):
                files = self.get_files_from_directory(directory)
                if not files:
                    print("Nenhum arquivo suportado encontrado na pasta.")
                    return
            else:
                print("Pasta não encontrada.")
                return
                
        elif choice == '2':
            print("Digite os caminhos dos arquivos (um por linha, linha vazia para terminar):")
            while True:
                file_path = input("Arquivo: ").strip()
                if not file_path:
                    break
                if os.path.exists(file_path):
                    extension = Path(file_path).suffix.lower()
                    if extension in self.supported_image_formats or extension == self.supported_pdf_format:
                        files.append(file_path)
                    else:
                        print(f"Formato não suportado: {extension}")
                else:
                    print("Arquivo não encontrado.")
        
        if not files:
            print("Nenhum arquivo válido selecionado.")
            return
        
        # Escolher método de ordenação
        print("\nComo você quer ordenar os arquivos?")
        print("1. Ordem alfabética (nome)")
        print("2. Data de modificação")
        print("3. Tamanho do arquivo")
        print("4. Ordem personalizada")
        print("5. Manter ordem atual")
        
        sort_choice = input("Escolha (1-5): ").strip()
        
        if sort_choice == '1':
            files = self.sort_files(files, 'name')
        elif sort_choice == '2':
            files = self.sort_files(files, 'date')
        elif sort_choice == '3':
            files = self.sort_files(files, 'size')
        elif sort_choice == '4':
            files = self.custom_sort_files(files)
        # Para '5' ou qualquer outra opção, mantém a ordem atual
        
        # Nome do arquivo de saída
        output_name = input("\nNome do arquivo PDF de saída (sem extensão): ").strip()
        if not output_name:
            output_name = "merged_document"
        
        output_path = f"{output_name}.pdf"
        
        # Confirmar antes de processar
        print(f"\nArquivos a serem processados ({len(files)}):")
        for i, file in enumerate(files, 1):
            print(f"{i}. {Path(file).name}")
        
        print(f"\nArquivo de saída: {output_path}")
        confirm = input("Processar? (s/n): ").strip().lower()
        
        if confirm == 's' or confirm == 'sim':
            print("\nProcessando...")
            if self.merge_files_to_pdf(files, output_path):
                print(f"✅ PDF criado com sucesso: {output_path}")
            else:
                print("❌ Erro ao criar PDF")
        else:
            print("Operação cancelada.")


def main():
    parser = argparse.ArgumentParser(description='Junta imagens e PDFs em um único arquivo PDF')
    parser.add_argument('-d', '--directory', help='Diretório com os arquivos')
    parser.add_argument('-f', '--files', nargs='+', help='Lista de arquivos específicos')
    parser.add_argument('-o', '--output', default='merged_document.pdf', help='Nome do arquivo de saída')
    parser.add_argument('-s', '--sort', choices=['name', 'date', 'size'], default='name',
                       help='Método de ordenação dos arquivos')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Modo interativo para seleção e ordenação')
    
    args = parser.parse_args()
    
    merger = PDFMerger()
    
    if args.interactive:
        merger.interactive_mode()
        return
    
    # Modo linha de comando
    files = []
    
    if args.directory:
        if os.path.exists(args.directory):
            files = merger.get_files_from_directory(args.directory)
        else:
            print(f"Diretório não encontrado: {args.directory}")
            return
    elif args.files:
        for file_path in args.files:
            if os.path.exists(file_path):
                extension = Path(file_path).suffix.lower()
                if extension in merger.supported_image_formats or extension == merger.supported_pdf_format:
                    files.append(file_path)
                else:
                    print(f"Formato não suportado ignorado: {file_path}")
            else:
                print(f"Arquivo não encontrado ignorado: {file_path}")
    else:
        print("Use -i para modo interativo ou especifique -d ou -f")
        return
    
    if not files:
        print("Nenhum arquivo válido encontrado.")
        return
    
    # Ordenar arquivos
    files = merger.sort_files(files, args.sort)
    
    print(f"Processando {len(files)} arquivos...")
    for file in files:
        print(f"  - {Path(file).name}")
    
    if merger.merge_files_to_pdf(files, args.output):
        print(f"✅ PDF criado com sucesso: {args.output}")
    else:
        print("❌ Erro ao criar PDF")


if __name__ == "__main__":
    main()
