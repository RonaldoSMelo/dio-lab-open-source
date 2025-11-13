#!/usr/bin/env python3
"""
Script de demonstração para testar a aplicação web PDF Merger
Cria arquivos de exemplo e inicia o servidor
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import tempfile
from pathlib import Path

def create_sample_images():
    """
    Cria imagens de exemplo para demonstração
    """
    print("📸 Criando imagens de exemplo...")
    
    # Criar diretório de exemplos
    examples_dir = Path("exemplos")
    examples_dir.mkdir(exist_ok=True)
    
    # Cores e textos para as imagens
    samples = [
        {"name": "pagina_1.png", "color": (255, 100, 100), "text": "PÁGINA 1\nEsta é a primeira página\ndo documento"},
        {"name": "pagina_2.jpg", "color": (100, 255, 100), "text": "PÁGINA 2\nEsta é a segunda página\ncom uma imagem JPG"},
        {"name": "pagina_3.png", "color": (100, 100, 255), "text": "PÁGINA 3\nTerceira página do\ndocumento final"},
        {"name": "capa.png", "color": (255, 200, 50), "text": "CAPA\nDocumento de Exemplo\nPDF Merger Web"},
        {"name": "contra_capa.jpg", "color": (200, 50, 255), "text": "CONTRA-CAPA\nFim do documento\nObrigado!"}
    ]
    
    created_files = []
    
    for sample in samples:
        try:
            # Criar imagem
            img = Image.new('RGB', (800, 600), sample["color"])
            draw = ImageDraw.Draw(img)
            
            # Tentar usar uma fonte melhor
            try:
                font = ImageFont.truetype("arial.ttf", 40)
                title_font = ImageFont.truetype("arial.ttf", 60)
            except:
                try:
                    font = ImageFont.truetype("Arial.ttf", 40)  # macOS
                    title_font = ImageFont.truetype("Arial.ttf", 60)
                except:
                    font = ImageFont.load_default()
                    title_font = font
            
            # Desenhar texto
            lines = sample["text"].split('\n')
            y_start = 200
            
            for i, line in enumerate(lines):
                current_font = title_font if i == 0 else font
                
                # Calcular posição central
                bbox = draw.textbbox((0, 0), line, font=current_font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (800 - text_width) // 2
                y = y_start + (i * 70)
                
                # Sombra
                draw.text((x+3, y+3), line, font=current_font, fill=(0, 0, 0))
                # Texto principal
                draw.text((x, y), line, font=current_font, fill=(255, 255, 255))
            
            # Salvar imagem
            file_path = examples_dir / sample["name"]
            img.save(file_path, quality=95)
            created_files.append(str(file_path))
            
            print(f"  ✅ Criado: {sample['name']}")
            
        except Exception as e:
            print(f"  ❌ Erro ao criar {sample['name']}: {e}")
    
    return created_files

def create_sample_pdf():
    """
    Cria um PDF de exemplo simples
    """
    print("📄 Criando PDF de exemplo...")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        
        examples_dir = Path("exemplos")
        examples_dir.mkdir(exist_ok=True)
        
        pdf_path = examples_dir / "documento_exemplo.pdf"
        
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        width, height = A4
        
        # Página 1
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredText(width/2, height-100, "DOCUMENTO PDF DE EXEMPLO")
        
        c.setFont("Helvetica", 16)
        c.drawCentredText(width/2, height-150, "Este é um PDF que será combinado com imagens")
        c.drawCentredText(width/2, height-180, "usando a interface web do PDF Merger")
        
        c.setFont("Helvetica", 12)
        y_pos = height - 250
        content = [
            "• Este documento demonstra a funcionalidade",
            "• Você pode arrastar este PDF junto com imagens",
            "• A ordem pode ser reorganizada via drag-and-drop",
            "• O resultado será um PDF unificado"
        ]
        
        for line in content:
            c.drawString(100, y_pos, line)
            y_pos -= 30
        
        c.showPage()
        
        # Página 2
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredText(width/2, height-100, "SEGUNDA PÁGINA DO PDF")
        
        c.setFont("Helvetica", 14)
        c.drawCentredText(width/2, height-150, "Esta é a segunda página do documento PDF de exemplo")
        
        c.save()
        
        print(f"  ✅ Criado: documento_exemplo.pdf")
        return str(pdf_path)
        
    except ImportError:
        print("  ⚠️  reportlab não instalado. PDF de exemplo não criado.")
        print("  💡 Instale com: pip install reportlab")
        return None
    except Exception as e:
        print(f"  ❌ Erro ao criar PDF: {e}")
        return None

def show_instructions():
    """
    Mostra instruções para usar a demonstração
    """
    print("\n" + "="*60)
    print("🎉 DEMONSTRAÇÃO PDF DA CINTIA MERGE WEB")
    print("="*60)
    print()
    print("📁 Arquivos de exemplo criados na pasta 'exemplos/':")
    print("   • Imagens coloridas com textos (PNG e JPG)")
    print("   • PDF de exemplo (se reportlab estiver instalado)")
    print()
    print("🌐 Para testar a aplicação:")
    print("   1. Execute: python app.py")
    print("   2. Abra: http://localhost:5000")
    print("   3. Arraste os arquivos da pasta 'exemplos'")
    print("   4. Reorganize a ordem arrastando os itens")
    print("   5. Clique em 'Gerar PDF' para criar o resultado")
    print()
    print("✨ Funcionalidades para testar:")
    print("   • Drag & drop de arquivos")
    print("   • Reordenação visual dos itens")
    print("   • Upload de múltiplos arquivos")
    print("   • Geração e download do PDF final")
    print()
    print("📱 Teste também em dispositivos móveis!")
    print("="*60)

def main():
    """
    Função principal da demonstração
    """
    print("🚀 Preparando demonstração do PDF da Cintia Merge Web...")
    print()
    
    # Criar arquivos de exemplo
    image_files = create_sample_images()
    pdf_file = create_sample_pdf()
    
    # Mostrar instruções
    show_instructions()
    
    # Perguntar se quer iniciar o servidor
    print("\n🔄 Deseja iniciar o servidor agora? (s/n): ", end="")
    try:
        response = input().strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            print("\n🌐 Iniciando servidor Flask...")
            import subprocess
            subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Demonstração cancelada.")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        print("💡 Execute manualmente: python app.py")

if __name__ == "__main__":
    main()
